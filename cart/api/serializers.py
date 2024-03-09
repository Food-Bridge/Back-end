from rest_framework import serializers
from cart.models import cart

class CartSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = cart
        fields = "__all__"