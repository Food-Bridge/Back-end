from django.db import models
from django.utils import timezone

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, help_text="실제 주문시 사용하는 쿠폰 코드")
    content = models.CharField(max_length=255, help_text="쿠폰 설명")
    minimum_order_price = models.PositiveIntegerField(default=0, help_text="쿠폰 사용 최소 금액")
    discount_price = models.PositiveIntegerField(default=0, help_text="쿠폰 할인 금액")
    expiration_date = models.DateTimeField(help_text="쿠폰 유효 기간")
    is_active = models.BooleanField(default=True)

    def expired(self):
        return timezone.now() > self.expiration_date

    def __str__(self):
        return self.code