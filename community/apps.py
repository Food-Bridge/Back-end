from django.apps import AppConfig
from django.conf import settings

class CommunityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'community'

    def ready(self):
        from community.api import jobs
        jobs.dailyschedule()
        jobs.weeklyschedule()