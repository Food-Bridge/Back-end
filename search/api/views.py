from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from restaurant.models import Restaurant
from restaurant.api.serializers import RestaurantSerializer
from search.api.serializers import SearchHistorySerializer
from rest_framework.filters import SearchFilter
from rest_framework import generics
from search.models import SearchHistory
from django.utils import timezone
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class RestaurantPagination(PageNumberPagination):
    page_size = 5

class RestaurantSearchAPI(generics.ListAPIView):
    pagination_class = RestaurantPagination
    serializer_class = RestaurantSerializer
    filter_backends = [SearchFilter]
    # 지점 이름으로 지정
    # TO-DO : 모델에 카테고리 추가해서 같이 검색될수 있도록 처리
    # api로 요청하면 1개씩 증가되는데, 페이지에서 호출하면 2개씩 처리된다 ;;
    search_fields = ['$name']

    def get_queryset(self):
        # orderCount 많은대로 정렬
        queryset = Restaurant.objects.all().order_by('-orderCount')
        search_query = self.request.query_params.get('search', None)
        
        if search_query:
            SearchHistory.objects.create(keyword=search_query)
        
        return queryset

class RestaurantCategorySearchAPI(generics.ListAPIView):
    pagination_class = RestaurantPagination
    serializer_class = RestaurantSerializer
    filter_backends = [SearchFilter]
    search_fields = ['mainCategory__name']
    
    def get_queryset(self):
        queryset = Restaurant.objects.all().order_by('-orderCount')
        return queryset
        
    
    
class SearchHistoryRankingAPI(generics.ListAPIView):
    serializer_class = SearchHistorySerializer  # 필요한 경우, SearchHistorySerializer를 적절하게 정의해야 합니다.

    def get_queryset(self):
        # 키워드별로 빈도수를 계산하여 순위를 생성하고 상위 10개만 가져옴
        queryset = SearchHistory.objects.values('keyword').annotate(search_count=Count('id')).order_by('-search_count')[:10]
        return queryset