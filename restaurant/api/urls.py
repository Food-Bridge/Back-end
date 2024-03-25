from django.urls import path
from restaurant.api.views import RestaurantAPIView, RestaurantDetailAPIView, RestaurantReviewAPIView

urlpatterns = [
    path('', RestaurantAPIView.as_view(), name="restaurant"),
    path('<int:pk>', RestaurantDetailAPIView.as_view(), name="restaurantDetail"),
    path('<int:pk>/reviews/', RestaurantReviewAPIView.as_view(), name="restaurantReview")
]