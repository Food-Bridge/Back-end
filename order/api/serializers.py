from rest_framework import serializers
from order.models import Order
from users.models import Address
from order.api.utils import get_estimated_time

class OrderSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    restaurant_name = serializers.ReadOnlyField(source="restaurant.name")
    restaurant_image = serializers.ImageField(
        source="restaurant.image", read_only=True
    )
    delivery_fee = serializers.ReadOnlyField(source="restaurant.deliveryFee")
    
    payment_method_name = serializers.CharField(
        source='get_payment_method_display', read_only=True
    )
    order_state_name = serializers.CharField(
        source='get_order_state_display', read_only=True
    )
    
    delivery_state_name = serializers.CharField(source='get_delivery_state_display', read_only=True)
    phonenumber = serializers.ReadOnlyField(source="user.phone_number", read_only=True)
    # estimate_time = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "phonenumber",
            "delivery_fee", 
            "restaurant_image", 
            "restaurant_name", 
            "required_options_count", 
            "menu_list", 
            "option_list", 
            "total_price",
            "coupon_code",
            "deliver_address",
            "deliveryman_request",
            "is_deliver",
            "delivery_state_name",
            "payment_method",
            "payment_method_name",
            "order_state", 
            "order_state_name",
            "review_written",
            "created_at", 
            "restaurant", 
            "order_id",
            # "estimate_time"
        ]

    # def get_estimate_time(self, obj):
    #     order_id = obj.id
    #     user = obj.user
    #     estimated_time_data = get_estimated_time(order_id, user)
    #     return estimated_time_data