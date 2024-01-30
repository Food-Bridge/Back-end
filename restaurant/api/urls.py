from django.urls import path
from restaurant.api.views import RestaurantAPIView

urlpatterns = [
    path('', RestaurantAPIView.as_view(), name="restaurant"),
]