from rest_framework import permissions, generics
from coupon.models import Coupon
from coupon.api.serializers import CouponSerializer
from rest_framework.exceptions import PermissionDenied

# Create your views here.
class CouponAPIView(generics.ListCreateAPIView):
    """
    GET : 
        쿠폰 리스트 조회
    ```
        - CODE : 실제 주문시 사용하는 쿠폰 코드
        - content : 쿠폰 설명
        - minimum_order_price : 최소 쿠폰 사용 금액
        - discount_price : 할인 금액
    ```
    POST : 
        쿠폰 추가 (주의)
        쿠폰관리는 민감하므로 admin 유저만 허용 하였음
    ```
        - CODE : 실제 주문시 사용할 쿠폰 코드
        - content : 쿠폰 설명
        - minimum_order_price : 최소 쿠폰 사용 금액
        - discount_price : 할인 금액
    ```
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    
    def create(self, request, *args, **kwargs):
        if not request.user.is_admin:
            raise PermissionDenied("You do not have permission to perform this action.")
        return super().create(request, *args, **kwargs)