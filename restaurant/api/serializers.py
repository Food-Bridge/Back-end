from rest_framework import serializers
from restaurant.models import Restaurant, MainCategory, SubCategory

class MainCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MainCategory
        fields = "__all__"
        
class SubCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SubCategory
        fields = "__all__"

class RestaurantSerializer(serializers.ModelSerializer):
    minDeliveryTimeMinutes = serializers.SerializerMethodField()
    maxDeliveryTimeMinutes = serializers.SerializerMethodField()
    
    mainCategory_name = serializers.SerializerMethodField()
    subCategory_name = serializers.SerializerMethodField()
    
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
            minDeliveryTimeMinutes =  obj.minDeliveryTime
            return minDeliveryTimeMinutes
        return None

    def get_maxDeliveryTimeMinutes(self, obj):
        if obj.maxDeliveryTime:
            maxDeliveryTimeMinutes =  obj.maxDeliveryTime
            return maxDeliveryTimeMinutes
        return None

    def get_mainCategory_name(self, obj):
        if obj.mainCategory:
            return obj.mainCategory.name
        return None

    def get_subCategory_name(self, obj):
        if obj.subCategory:
            return obj.subCategory.name
        return None
    
    class Meta:
        model = Restaurant
        exclude = ('minDeliveryTime', 'maxDeliveryTime')
