from community.api.views import DailyPopularPostAPIView, WeekPopularPostAPIView
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings

def update_daily_popular_posts():
    try:
        daily_popular_view = DailyPopularPostAPIView()
        response = daily_popular_view.get(None)
        serializer_data = response.data
        print(serializer_data)
        print("일간 인기글이 갱신이 되었습니다.")
        return serializer_data
    except Exception as e:
        print(f"Error updating daily popular posts: {e}")
        return None

def update_weekly_popular_posts():
    try:
        weekly_popular_view = WeekPopularPostAPIView()
        response = weekly_popular_view.get(None)
        serializer_data = response.data
        print(serializer_data)
        print("주간 인기글이 갱신되었습니다.")
        return serializer_data
    except Exception as e:
        print(f"Error updating weekly popular posts: {e}")
        return None

def dailyschedule():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_job(update_daily_popular_posts, 'interval', days=1)
    scheduler.start()

def weeklyschedule():
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_job(update_weekly_popular_posts, 'interval', weeks=1)
    scheduler.start()