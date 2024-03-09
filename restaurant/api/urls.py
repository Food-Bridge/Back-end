from django.urls import path
from restaurant.api.views import RestaurantAPIView, RestaurantDetailAPIView

urlpatterns = [
    path('', RestaurantAPIView.as_view(), name="restaurant"),
    path('<int:pk>', RestaurantDetailAPIView.as_view(), name="restaurantDetail")
]