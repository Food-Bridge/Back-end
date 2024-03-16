from rest_framework import serializers
from order.models import Order, UserOrderReview

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
    
    delivery_state_name = serializers.CharField(
        source='get_delivery_state_display', read_only=True
    )
    
    class Meta:
        model = Order
        fields = [
            "id",
            "user", 
            "delivery_fee", 
            "restaurant_image", 
            "restaurant_name", 
            "required_options_count", 
            "menu_list", 
            "option_list", 
            "total_price", 
            "deliveryman_request",
            "is_deliver",
            "delivery_state_name",
            "payment_method",
            "payment_method_name",
            "order_state", 
            "order_state_name", 
            "created_at", 
            "restaurant", 
            "order_id"
        ]

class ReviewSerializer(serializers.ModelSerializer):
    order_id = serializers.PrimaryKeyRelatedField(source='order.id', read_only=True)  # queryset 인자 제거

    class Meta:
        model = UserOrderReview
        fields = ['content', 'order_id', 'id',]  # order_id 필드를 'fields'에 명시