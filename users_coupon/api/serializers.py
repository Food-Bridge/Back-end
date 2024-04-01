from rest_framework import serializers
from users_coupon.models import UserCoupon

class UserCouponSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")
    coupon_id = serializers.ReadOnlyField(source='coupon.id')
    coupon_code = serializers.ReadOnlyField(source="coupon.code")
    coupon_expire = serializers.ReadOnlyField(source='coupon.expiration_date')
    discount_price = serializers.ReadOnlyField(source='coupon.discount_price')
    minimum_order_price = serializers.ReadOnlyField(source='coupon.minimum_order_price')

    class Meta:
        model = UserCoupon
        fields = ["id", "user", "coupon_id" , "coupon_code", "coupon_expire", "discount_price", "minimum_order_price",]