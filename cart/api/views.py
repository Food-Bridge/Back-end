from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from cart.models import cart
from .serializers import CartSerializer

class CartAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    1. menu_list : 메뉴 리스트
    2. option_list : 옵션 리스트
    3. total_price : 최종 금액
    4. deliveryman_request : 배송시 요청 사항
    5. paymentMethod : credit_card, cash
    6. restaurant : 레스토랑 id
    
    메뉴 2개, 옵션 2개 이상일 경우의 예
    ```
    {
    "menu_list":
        {
            "menu_id: 1,
            "menu_name" : "양념치킨",
            "price" : 15000 ,
            "quantity" : 1 
        },
        {
            "menu_id": 3,
            "menu" : "간장치킨",
            "price" : 17000,
            "quantity" : 1
        }
    "option_list":
        {
            "option_id": 1,
            "option_name" : "소스 추가"
            "price" : 1000 ,
            "quantity" : 1
        },
        {
            "option_id": 10,
            "option_name" : "치킨 무 추가"
            "price" : 0,
            "quantity" : 1
        },
    ...
    ```
    }
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
        user = self.request.user
        
        # 기존 장바구니에 데이터 있을 경우 데이터 삭제
        existing_cart = self.get_object()
        if existing_cart:
            existing_cart.delete() 
        
        if user.is_authenticated:
            request.data["user"] = user.id
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "인증이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)