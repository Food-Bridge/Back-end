from django.db import models
from django.utils import timezone

class Coupon(models.Model):
    name = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    minimum_order_price = models.IntegerField(default=0)
    discount_price = models.IntegerField(default=0)
    expiration_date = models.DateTimeField()

    def expired(self):
        return timezone.now() > self.expiration_date
    
    def __str__(self):
        return self.name