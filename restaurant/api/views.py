from restaurant.api.serializers import RestaurantSerializer
from restaurant.models import Restaurant
from rest_framework import permissions, generics

class RestaurantAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()

class RestaurantDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()