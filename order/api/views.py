from rest_framework import permissions, generics, status
from rest_framework.response import Response
from django.utils import timezone
from order.models import Order
from restaurant.models import Restaurant
from coupon.models import Coupon
from menu.models import Menu, MenuOption
from order.api.serializers import OrderSerializer

class OrderAPIView(generics.ListCreateAPIView):
    """
    1. menu_list : 메뉴 리스트
    2. option_list : 옵션 리스트
    3. total_price : 최종 금액
    4. deliveryman_request : 배송시 요청 사항
    5. required_options_count : 최소 필수 주문 개수
    6. payment_method : credit_card, cash
    7. restaurant : 레스토랑 id
    8. coupon_code : 쿠폰코드
    
    메뉴 2개, 옵션 2개 이상일 경우의 예
    ```
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
        required_options_count = request.data.get('required_options_count') # 필수 옵션 개수 가져오기
        coupon_code = request.data.get('coupon_code') # 쿠폰 코드 가져오기

        # 현재 사용자 정보 가져오기
        user = request.user

        # 주문할 음식점이 유효한지 확인
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response({'error': '유효하지 않은 음식점입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        # 메뉴와 옵션을 저장할 리스트 초기화
        menus = []
        options = []
        total_price = 0
        order_id = timezone.now().strftime("%Y%m%d%H") + "_" + str(user.id)

        if required_options_count is None:
            return Response({'error': "필수 주문 값을 받지 못했습니다."}, status=status.HTTP_400_BAD_REQUEST)

        if len(menu_data) == 0:
            return Response({'error': "필수 주문 데이터가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        if required_options_count > len(menu_data) :
            return Response({'error': "필수 주문 데이터가  부족합니다."}, status=status.HTTP_400_BAD_REQUEST)

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
            'menu_list' : menu_data,
            'option_list' : option_data,
            'order_id' : order_id
        }
        order_serializer = OrderSerializer(data=order_data)

        if order_serializer.is_valid():
            order_serializer.save()
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
