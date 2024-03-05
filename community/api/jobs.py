from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, F
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PopularPostSerializer
from community.models import Blog
from community.api.views import DailyPopularPostAPIView
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings

def update_daily_popular_posts():
    try:
        daily_popular_view = DailyPopularPostAPIView()
        response = daily_popular_view.get(None)
        serializer_data = response.data
        print(serializer_data)
        print("갱신이 되었습니다.")
        return serializer_data
    except Exception as e:
        print(f"Error updating daily popular posts: {e}")
        return None

def schedule():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    # 빠른 확인을 위해 인터벌을 5초로 지정
    scheduler.add_job(update_daily_popular_posts, 'interval', seconds=5)
    scheduler.start()