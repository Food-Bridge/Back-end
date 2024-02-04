from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from restaurant.models import Restaurant
from restaurant.api.serializers import RestaurantSerializer
from rest_framework.filters import SearchFilter
from rest_framework import generics, filters
from search.models import SearchHistory
from django.utils import timezone

class RestaurantSearchAPI(generics.ListAPIView):
    serializer_class = RestaurantSerializer
    filter_backends = [SearchFilter]
    # 지점 이름으로 지정
    # TO-DO : 모델에 카테고리 추가해서 같이 검색될수 있도록 처리
    # api로 요청하면 1개씩 증가되는데, 페이지에서 호출하면 2개씩 처리된다 ;;
    search_fields = ['$name']
    
    def get_queryset(self):
        # 주문수 많은대로 정렬
        queryset = Restaurant.objects.all().order_by('-orderCount')
        search_query = self.request.query_params.get('search', None)
        if search_query:
            try:
                # 검색 히스토리 저장
                search_history = SearchHistory.objects.get(keyword=search_query)
                # 이미 존재하는 검색어라면 검색 횟수를 1 증가시킴
                search_history.search_count += 1
                search_history.save()
            except SearchHistory.DoesNotExist:
                # 새로운 검색어라면 검색 횟수를 1로 설정
                SearchHistory.objects.create(keyword=search_query, search_count=1)
            # 검색 키워드가 존재할 때만 필터링
            queryset = queryset.filter(name__icontains=search_query)
        return queryset