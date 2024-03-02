from rest_framework import serializers
from coupon.models import Coupon

class CouponSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    formatted_expiration_date = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        fields = ['id', 'name', 'content', 'minimum_order_price', 'discount_price', 'status', 'formatted_expiration_date']

    def get_status(self, obj):
        return not obj.expired()
    
    def get_formatted_expiration_date(self, obj):
        return obj.expiration_date.strftime('%Y년 %m월 %d일까지')