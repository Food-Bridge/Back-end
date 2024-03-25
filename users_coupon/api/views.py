from rest_framework import generics, permissions
from users_coupon.api.serializers import UserCouponSerializer
from users_coupon.models import UserCoupon

# Create your views here.
class UserCouponAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserCouponSerializer
    queryset =UserCoupon.objects.all()

    def get_queryset(self):
        user_id = self.request.user.id
        return UserCoupon.objects.filter(user_id=user_id)