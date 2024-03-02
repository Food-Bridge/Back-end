from rest_framework import serializers
from cart.models import cart

class CartSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")
    
    class Meta:
        model = cart
        fields = ['id', 'user', 'menu_id', 'menu_name', 'menu_price', 'amount', 'total_price', 'option_name', 'option_price', 'restaurant_id']