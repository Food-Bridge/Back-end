from django.db import models
from django.utils import timezone

# Create your models here.
class Coupon(models.Model):
    name = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    minimumOrderPrice = models.IntegerField(default=0)
    discountPrice = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expiration_date