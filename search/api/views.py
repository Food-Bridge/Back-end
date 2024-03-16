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
from rest_framework.permissions import AllowAny
from datetime import timedelta

class RestaurantPagination(PageNumberPagination):
    page_size = 5

class RestaurantSearchAPI(generics.ListAPIView):
    pagination_class = RestaurantPagination
    serializer_class = RestaurantSerializer
    filter_backends = [SearchFilter]
    permission_classes = [AllowAny]
    
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
    """
    메인카테고리 번호에 해당하는 값을 검색하면 해당하는 레스토랑이 출력되는 API
    search/category/?search=1
    """
    pagination_class = RestaurantPagination
    serializer_class = RestaurantSerializer
    filter_backends = [SearchFilter]
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        category_number = self.request.GET.get('search')
        queryset = Restaurant.objects.filter(mainCategory=category_number).order_by('-orderCount')
        return queryset
        
    
    
class SearchHistoryRankingAPI(generics.ListAPIView):
    serializer_class = SearchHistorySerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        # 1시간 전의 시간 계산
        one_hour_ago = timezone.now() - timedelta(minutes=60)

        # 1시간 전까지의 검색어 순위를 저장
        previous_rankings = list(SearchHistory.objects.filter(created_at__lte=one_hour_ago).values('keyword').annotate(search_count=Count('id')).order_by('-search_count')[:10])

        # 현재 검색어 순위 계산
        current_rankings = list(SearchHistory.objects.values('keyword').annotate(search_count=Count('id')).order_by('-search_count')[:10])

        # 순위 변동 계산
        for i, keyword_data in enumerate(current_rankings):
            keyword_data['previous_rank'] = next((index + 1 for index, item in enumerate(previous_rankings) if item['keyword'] == keyword_data['keyword']), None)
            if keyword_data['previous_rank'] is not None:
                rank_change = keyword_data['previous_rank'] - (i + 1)
                keyword_data['rank_change'] = "up" if rank_change > 0 else None if rank_change < 0 else "same"
            else:
                keyword_data['rank_change'] = None
            keyword_data['rank'] = i + 1
            
        return current_rankings
