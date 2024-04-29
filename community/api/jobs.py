from community.api.views import DailyPopularPostAPIView, WeekPopularPostAPIView
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings

def update_daily_popular_posts():
    try:
        daily_popular_view = DailyPopularPostAPIView()
        response = daily_popular_view.get(None)
        serializer_data = response.data
        return serializer_data
    except Exception as e:
        return None

def update_weekly_popular_posts():
    try:
        weekly_popular_view = WeekPopularPostAPIView()
        response = weekly_popular_view.get(None)
        serializer_data = response.data
        return serializer_data
    except Exception as e:
        return None

def dailyschedule():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_job(update_daily_popular_posts, 'interval', days=1)
    scheduler.start()

def weeklyschedule():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_job(update_weekly_popular_posts, 'interval', weeks=1)
    scheduler.start()