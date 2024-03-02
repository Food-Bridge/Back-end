from rest_framework import serializers
from users_coupon.models import UserCoupon

class UserCouponSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")
    coupon_id = serializers.ReadOnlyField()

    class Meta:
        model = UserCoupon
        fields = ["id", "coupon", "user", "coupon_id"]
