from django.urls import path
from search.api.views import RestaurantSearchAPI

urlpatterns = [
    path('', RestaurantSearchAPI.as_view(), name="search"),
]