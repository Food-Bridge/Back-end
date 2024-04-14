from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from cart.models import cart
from restaurant.models import Restaurant
from menu.models import Menu, MenuOption, MenuSelectedOption
from .serializers import CartSerializer

class CartAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    1. menu_list : 메뉴 리스트
    2. option_list : 옵션 리스트
    3. soption_list : 선택 옵션 리스트
    4. total_price : 최종 금액
    5. deliveryman_request : 배송시 요청 사항
    6. restaurant : 레스토랑 id
    
    메뉴 2개, 옵션 2개 이상일 경우의 예
    {
    "menu_list": [
        {
        "menu_id": 1,
        "menu_name": "양념치킨",
        "price": 15000,
        "quantity": 1
        },
        {
        "menu_id": 3,
        "menu_name": "간장치킨",
        "price": 17000,
        "quantity": 1
        }
    ],
    "option_list": [
        {
        "option_id": 1,
        "option_name": "소스 추가",
        "price": 1000,
        "quantity": 1
        }
    ],
    "soption_list": [
        {
        "option_id": 1,
        "option_name": "소스 추가",
        "price": 1000,
        "quantity": 1
        }
    ],
    "total_price": 0,
    "restaurant": 1
    }
    ```
    """
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        user = self.request.user
        if user.is_authenticated:
            try:
                obj = cart.objects.get(user=user)
                return obj
            except cart.DoesNotExist:
                return None
        else:
            return None

    def post(self, request, *args, **kwargs):
        restaurant_id = request.data.get('restaurant')
        menu_data = request.data.get('menu_list', [])  # 메뉴 데이터 가져오기
        option_data = request.data.get('option_list', [])  # 옵션 데이터 가져오기
        soption_data = request.data.get('soption_list', []) # 선택 옵션 데이터 가져오기
        
        # 장바구니에 저장할 음식점이 유효한지 확인
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response({'error': '유효하지 않은 음식점입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 메뉴와 옵션을 저장할 리스트 초기화
        menus = []
        options = []
        soptions = []
        total_price = 0
        
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

        # 장바구니 데이터 생성
        cart_data = {
            'user': request.user.id,
            'restaurant': request.data.get('restaurant'),
            'menu_list' : menu_data,
            'option_list' : option_data,
            'soption_list' : soption_data,
            'total_price': total_price,
        }
        cart_serializer = CartSerializer(data=cart_data)
        
        # 기존 장바구니에 데이터 있을 경우 데이터 삭제
        existing_cart = self.get_object()
        if existing_cart:
            existing_cart.delete() 
        
        if cart_serializer.is_valid():
            cart_serializer.save()
            return Response(cart_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)