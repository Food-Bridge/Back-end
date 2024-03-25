from rest_framework import generics, permissions
from users_coupon.api.serializers import UserCouponSerializer
from users_coupon.models import UserCoupon

# Create your views here.
class UserCouponAPIView(generics.ListAPIView):
    """
    유저가 보유하고 있는 쿠폰 조회
    결과 예시)
    [
        {
            "id": 1,
            "coupon": 1,
            "user": 2,
            "coupon_id": 1
        }
    ]
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserCouponSerializer
    queryset =UserCoupon.objects.all()

    def get_queryset(self):
        user_id = self.request.user.id
        return UserCoupon.objects.filter(user_id=user_id)