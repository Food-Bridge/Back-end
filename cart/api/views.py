from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from cart.models import cart
from .serializers import CartSerializer

class CartAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    json 전송 예시
    1. food_id : 메뉴 번호
    2. food_name : 메뉴 이름
    3. food_price : 메뉴 가격 (고정)
    4. amount : 수량 (food_price 값과 조합)
    5. option_name : 옵션 이름
    6. option_price : value 값을 합산하여 total_price에 추가 적용 
    
    {
    "food_id": 1001,
    "food_name": "간장치킨",
    "food_price": 3000,
    "amount": 2,
    "option_name":
            { 
                "1" : "중간맛",
                "2" : "치킨무 추가" ,
                "3" : "소스 추가" 
            },
    "option_price":
            {
                "1": 1000,
                "2": 0,
                "3": 1500
            },
    "restaurant_id" : 3
    }
    """
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        user = self.request.user
        if user.is_authenticated:
            obj, created = cart.objects.get_or_create(user=user)
            return obj
        else:
            return None  # 인증되지 않은 경우에는 None 반환

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
            return Response({"detail": "인증이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)