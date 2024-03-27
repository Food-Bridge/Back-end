from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from users_coupon.api.serializers import UserCouponSerializer
from users_coupon.models import UserCoupon
from coupon.models import Coupon

class UserCouponAPIView(generics.ListCreateAPIView):
    """
    GET : 
        유저가 보유하고 있는 쿠폰 조회
    ```
        - CODE : 실제 주문시 사용하는 쿠폰 코드
        - content : 쿠폰 설명
        - minimum_order_price : 최소 쿠폰 사용 금액
        - discount_price : 할인 금액
    ```
    POST : 
        유저가 쿠폰 발급 요청
    ```
        - CODE : 실제 주문시 사용할 쿠폰 코드
    ```
    
    ```
    등록 예시
    {
        "CODE" : "PRICE1000"
    }
    ```
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserCouponSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return UserCoupon.objects.filter(user_id=user_id)
    
    
    def create(self, request, *args, **kwargs):
        code = request.data.get('code')
        user_id = self.request.user.id

        if code is None:
            return Response({'error': '쿠폰 코드를 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            return Response({'error': '해당 쿠폰을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        # 발급 받으려는 쿠폰이 유효한지 확인
        if not (coupon.is_active and coupon.expiration_date > timezone.now()):
            return Response({'error': '유효하지 않은 쿠폰입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 이미 해당 쿠폰을 가지고 있는지 확인
        if UserCoupon.objects.filter(user_id=user_id, coupon__code=code).exists():
            return Response({'error': '유저가 이미 해당 쿠폰을 가지고 있습니다'}, status=status.HTTP_400_BAD_REQUEST)

        # 쿠폰 발급
        try:
            user_coupon = UserCoupon.objects.create(user_id=user_id, coupon=coupon)
            serializer = UserCouponSerializer(user_coupon)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)