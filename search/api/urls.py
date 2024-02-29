from django.urls import path
from search.api.views import RestaurantSearchAPI, SearchHistoryRankingAPI, RestaurantCategorySearchAPI

urlpatterns = [
    path('', RestaurantSearchAPI.as_view(), name="search"),
    path('search-ranking/', SearchHistoryRankingAPI.as_view(), name='search-ranking'),
    path('category/', RestaurantCategorySearchAPI.as_view(), name='category'),
]