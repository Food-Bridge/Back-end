from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from .views import DailyPopularPostsAPIView

sched = BackgroundScheduler()

##### 인기글 작업 보류
# def period():
#     DailyPopularPostsAPIView

# def start():
#     sched.add_job(period, 'interval', seconds=10)
#     sched.start()