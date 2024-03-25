from rest_framework import permissions, generics

from restaurant.api.serializers import RestaurantSerializer
from restaurant.models import Restaurant
from review.models import Review
from review.api.serializers import ReviewSerializer


class RestaurantAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()

class RestaurantDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    
class RestaurantReviewAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        restaurant_id = self.kwargs['pk']
        return Review.objects.filter(restaurant_id=restaurant_id)