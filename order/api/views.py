import requests

from datetime import datetime
from urllib.parse import urlparse
from django.conf import settings
from django.utils import timezone
from django.db.models import F

from order.models import Order
from restaurant.models import Restaurant
from users.models import Address
from coupon.models import Coupon
from menu.models import Menu, MenuOption, MenuSelectedOption

from rest_framework import permissions, generics, status, views, reverse, serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from order.api.serializers import OrderSerializer
from order.api.utils import get_estimated_time
from users.api.utils import geocode_address
from django.shortcuts import redirect

class OrderAPIView(generics.ListCreateAPIView):
    """
    - user 값 넣지 않아도, 요청한 유저의 주문으로 들어감
    1. menu_list : 메뉴 리스트
    2. option_list : 옵션 리스트
    2-1. sopttion_list : 선택 옵션 리스트
    3. total_price : 최종 금액
    4. deliveryman_request : 배송시 요청 사항
    5. required_options_count : 최소 필수 주문 개수
    6. payment_method : credit_card, cash
    7. restaurant : 레스토랑 id
    8. coupon_code : 쿠폰코드 (없을 경우 null로)
    9. restaurant_request : 매장 요청 사항
    10. disposable_request : 일회용품 요청
    
    메뉴 1개, 옵션 1개, 선택옵션 1개 이상일 경우의 예
    ```
    "deliver_address" : "배달 주소",
    "coupon_code": "USERSIGNUP",
    {
        "menu_list" : [
            {
            "menu_id": 1,
            "menu_name": "양념치킨",
            "price": 15000,
            "quantity": 1 
        }
    ],
    "option_list" : [
        {
            "option_id": 1,
            "option_name": "소스 추가",
            "price": 1000,
            "quantity": 1
        }
    ],
    "soption_list": [
        { 
            "option_id" : 1, 
            "option_name" :"사이드",
            "price" : 1000,
            "quantity" : 1 
        }
    ],
    "name": "양념 치킨",
    "price": 15000,
    "content": null,
    "image": null,
    "required_options_count": 1,
    "is_main": false,
    "is_popular": false,
    "restaurant": 1,
    "order_state" : "order_complete",
    "payment_method" : "cash",
    "restaurant": 0,
    }
    ```
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)

    def post(self, request, *args, **kwargs):
        restaurant_id = request.data.get('restaurant')
        menu_data = request.data.get('menu_list', [])  # 메뉴 데이터 가져오기
        option_data = request.data.get('option_list', [])  # 옵션 데이터 가져오기
        soption_data = request.data.get('soption_list', []) # 선택 옵션 데이터 가져오기
        coupon_code = request.data.get('coupon_code') # 쿠폰 코드 가져오기
        deliver_address = request.data.get('deliver_address') # 배달 주소 가져오기

        # 현재 사용자 정보 가져오기
        user = request.user
        
        try:
            # 유저의 기본 주소 여부 확인
            user = Address.objects.get(user=user.id, is_default=True)
        except Address.DoesNotExist:
            return Response({'error': '유저의 기본 주소가 등록되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            

        # 주문할 음식점이 유효한지 확인
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response({'error': '유효하지 않은 음식점입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        # 메뉴와 옵션을 저장할 리스트 초기화
        menus = []
        options = []
        soptions = []
        total_price = 0
        order_id = timezone.now().strftime("%Y%m%d%H") + "_" + str(user.id)

        if len(menu_data) == 0:
            return Response({'error': "필수 주문 데이터가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 메뉴 데이터 처리
        for menu_item in menu_data:
            menu_id = menu_item.get('menu_id')
            menu_price = menu_item.get('price')
            menu_quantity = menu_item.get('quantity')
            try:
                menu = Menu.objects.get(id=menu_id, restaurant=restaurant)
                menus.append(menu)
                total_price += menu_price * menu_quantity  # 메뉴 가격과 수량을 곱하여 총 가격에 더함
            except Menu.DoesNotExist:
                return Response({'error': '음식점에 속하지 않은 메뉴가 주문되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 옵션 데이터 처리
        for option_item in option_data:
            option_id = option_item.get('option_id')
            option_price = option_item.get('price')
            option_quantity = option_item.get('quantity')
            try:
                option = MenuOption.objects.get(id=option_id)
                options.append(option)
                total_price += option_price * option_quantity  # 옵션 가격과 수량을 곱하여 총 가격에 더함
            except MenuOption.DoesNotExist:
                return Response({'error': '존재하지 않는 옵션이 주문되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 선택 옵션 데이터 처리
        for option_item in soption_data:
            option_id = option_item.get('option_id')
            option_price = option_item.get('price')
            option_quantity = option_item.get('quantity')
            try:
                option = MenuSelectedOption.objects.get(id=option_id)
                soptions.append(option)
                total_price += option_price * option_quantity  # 옵션 가격과 수량을 곱하여 총 가격에 더함
            except MenuSelectedOption.DoesNotExist:
                return Response({'error': '존재하지 않는 선택 옵션이 주문되었습니다'}, status=status.HTTP_400_BAD_REQUEST)


        # 쿠폰 코드가 유효한지 확인
        if coupon_code is not None:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                if coupon.expiration_date < timezone.now():
                    return Response({'error': "입력한 쿠폰의 유효기간이 지났습니다."}, status=status.HTTP_400_BAD_REQUEST)

                # 쿠폰가격을 최종 가격에 적용
                total_price = total_price - coupon.discount_price
                if total_price <= 0:
                    total_price = 0
            except Coupon.DoesNotExist:
                return Response({'error': '유효하지 않은 쿠폰 코드입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 주문 생성
        order_data = {
            'user': user.id,
            'restaurant': request.data.get('restaurant'),
            'total_price': total_price,
            'deliveryman_request': request.data.get('deliveryman_request'),
            'payment_method': request.data.get('payment_method'),
            'order_state': request.data.get('order_state'),
            'deliver_address' : deliver_address,
            'menu_list' : menu_data,
            'option_list' : option_data,
            'soption_list' : soption_data,
            'order_id' : order_id
        }
        order_serializer = OrderSerializer(data=order_data)

        if order_serializer.is_valid():
            # 주문 데이터가 유효한 경우
            order_instance = order_serializer.save()  # 주문을 저장하고 인스턴스를 반환합니다.
            # 해당 식당의 주문 수 증가
            Restaurant.objects.filter(pk=restaurant_id).update(orderCount=F('orderCount') + 1)

            # 배달 주소 위경도 처리
            if deliver_address:
                try:
                    geocoded_data = geocode_address(deliver_address)
                    if geocoded_data:
                        if geocoded_data['latitude'] == 127:
                            return Response({'erro': "배달 주소를 다시 입력해주세요"}, status=status.HTTP_400_BAD_REQUEST)
                        order_instance.latitude = geocoded_data.get('latitude')
                        order_instance.longitude = geocoded_data.get('longitude')
                        order_instance.save()
                except requests.exceptions.RequestException as e:
                    return Response({'error': f"Error during geocoding: {e}"}, status=status.HTTP_400_BAD_REQUEST)
            
            response = get_estimated_time(order_instance.id, user)
            order_serializer.data['estimate_time'] = response
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        else:
            # 주문 데이터가 유효하지 않은 경우
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()