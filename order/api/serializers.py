from rest_framework import serializers
from order.models import Order

class OrderSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Order
        fields = ["user", "menu_list", "option_list", "total_price", "deliveryman_request", "paymentMethod", "order_state", "created_at", "restaurant"]
        
