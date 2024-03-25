from rest_framework import permissions, generics
from coupon.models import Coupon
from coupon.api.serializers import CouponSerializer

# Create your views here.
class CouponAPIView(generics.ListCreateAPIView):
    """
    POST :
        CODE : 실제 주문시 사용하는 쿠폰 코드
        content : 쿠폰 설명
        minimum_order_price : 최소 쿠폰 사용 금액
        discount_price : 할인 금액
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer