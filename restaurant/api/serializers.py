from rest_framework import serializers
from restaurant.models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    minDeliveryTimeMinutes = serializers.SerializerMethodField()
    maxDeliveryTimeMinutes = serializers.SerializerMethodField()

    def validate_minDeliveryTimeMinutes(self, minDeliveryTimeMinutes):
        if minDeliveryTimeMinutes < 0:
            raise serializers.ValidationError('최소 배달 예상 시간이 음수가 나올 수 없습니다.')
        return minDeliveryTimeMinutes
    
    def validate_maxDeliveryTimeMinutes(self, maxDeliveryTimeMinutes):
        if maxDeliveryTimeMinutes > 70:
            raise serializers.ValidationError('최대 배달 예상 시간이 1시간 10분을 넘을 수 없습니다.')
        return maxDeliveryTimeMinutes

    def get_minDeliveryTimeMinutes(self, obj):
        if obj.minDeliveryTime:
            minDeliveryTimeMinutes =  obj.minDeliveryTime.hour * 60 + obj.minDeliveryTime.minute
            return minDeliveryTimeMinutes
        return None

    def get_maxDeliveryTimeMinutes(self, obj):
        if obj.maxDeliveryTime:
            maxDeliveryTimeMinutes =  obj.maxDeliveryTime.hour * 60 + obj.maxDeliveryTime.minute
            return maxDeliveryTimeMinutes
        return None

    class Meta:
        model = Restaurant
        exclude = ('minDeliveryTime', 'maxDeliveryTime')
