from django.db import models
from django.utils import timezone

class Coupon(models.Model):
    code = models.CharField(max_length=50)
    content = models.CharField(max_length=255)
    minimum_order_price = models.IntegerField(default=0)
    discount_price = models.IntegerField(default=0)
    expiration_date = models.DateTimeField()

    def expired(self):
        return timezone.now() > self.expiration_date

    def save(self, *args, **kwargs):
        # 쿠폰 발급 후 이틀 후의 날짜와 시간 설정
        self.expiration_date = timezone.now() + timezone.timedelta(days=2)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code