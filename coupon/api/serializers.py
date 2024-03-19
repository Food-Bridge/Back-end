from rest_framework import serializers
from coupon.models import Coupon

class CouponSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    formatted_expiration_date = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        fields = [
            'id',
            'code',
            'content',
            'minimum_order_price',
            'discount_price',
            'status',
            'formatted_expiration_date'
        ]

    ##### 쿠폰 만료 상태
    def get_status(self, obj):
        return not obj.expired()
    
    ##### 쿠폰 만료기간 파싱
    def get_formatted_expiration_date(self, obj):
        return obj.expiration_date.strftime('%Y년 %m월 %d일까지')