from django.db import models

class SearchHistory(models.Model):
    keyword = models.CharField(max_length=255)
    search_count = models.IntegerField(default=0)
    created_day = models.DateField(auto_now_add=True)
    created_hour = models.TimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']