from rest_framework import serializers
from cart.models import cart

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = cart
        fields = ['id', 'food_id', 'food_name', 'food_price', 'amount', 'total_price', 'option_name', 'option_price', 'restaurant_id']