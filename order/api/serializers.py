from rest_framework import serializers
from order.models import Order

class OrderSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.ReadOnlyField(source="restaurant.name")
        
    class Meta:
        model = Order
        fields = ["user", "restaurant_name", "required_options_count", "menu_list", "option_list", "total_price", "deliveryman_request", "paymentMethod", "order_state", "created_at", "restaurant", "order_id"]