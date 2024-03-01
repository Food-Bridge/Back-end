from rest_framework import serializers
from cart.models import cart

class CartSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")
    
    class Meta:
        model = cart
        fields = ['id', 'user', 'food_id', 'food_name', 'food_price', 'amount', 'total_price', 'option_name', 'option_price', 'restaurant_id']