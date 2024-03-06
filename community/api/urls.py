from django.urls import path, include
from .views import (CreatePostAPIView, 
                    ListPostAPIView, 
                    DetailPostAPIView, 
                    ListCommentAPIView, 
                    CreateCommentAPIView,
                    DetailCommentAPIView,
                    LikeAPIView,
                    LatestPostsAPIView,
                    DailyPopularPostAPIView,
                    WeekPopularPostAPIView,
)
urlpatterns = [
    path("", ListPostAPIView.as_view(), name="list_post"),
    path("create/", CreatePostAPIView.as_view(), name="create_post"),
    path("<int:pk>/", DetailPostAPIView.as_view(), name="detail_post"),
    path("<int:pk>/comment/", ListCommentAPIView.as_view(), name="list_comment"),
    path("<int:pk>/comment/create/", CreateCommentAPIView.as_view(), name="create_comment"),
    path("<int:pk>/comment/<int:id>/", DetailCommentAPIView.as_view(), name="detail_comment"),
    path("<int:pk>/likes/", LikeAPIView.as_view(), name="like"),
    path("latest/", LatestPostsAPIView.as_view(), name="latest_posts"),
    path("daily/", DailyPopularPostAPIView.as_view(), name="daily"),
    path("weekly/", WeekPopularPostAPIView.as_view(), name="week"),
]
