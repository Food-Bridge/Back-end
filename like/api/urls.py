from django.urls import path, include
from .views import LikeAPIView, LikeCreateAPIView

urlpatterns = [
    path("", LikeAPIView.as_view(), name="likelist"), # 좋아요 목록 보기
    path("<int:pk>/", LikeCreateAPIView.as_view(), name="likecreate"),
]