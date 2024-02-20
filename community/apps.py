from django.apps import AppConfig
from django.conf import settings

class CommunityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'community'

    # def ready(self):
    #     from community.api.operators import start
    #     start()