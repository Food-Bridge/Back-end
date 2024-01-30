from rest_framework import serializers
from coupon.models import Coupon
from django.utils import timezone

class CouponSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        fields = ['id', 'name', 'content', 'minimumOrderPrice', 'discountPrice', 'created_at', 'expiration_date', 'status']

    def get_status(self, obj):
        return not obj.is_expired()

    def get_deleted_at(self, obj):
        return None if not obj.is_expired() else timezone.now()
