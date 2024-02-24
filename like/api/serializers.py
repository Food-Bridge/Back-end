from rest_framework import serializers
from restaurant.models import Restaurant, MainCategory, SubCategory
from ..models import RestaurantLike

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantLike
        fields = ('restaurant', 'user',)