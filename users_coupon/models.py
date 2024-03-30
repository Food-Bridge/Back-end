from django.db import models
from coupon.models import Coupon
from users.models import User

class UserCoupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 사용자
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)  # 쿠폰
    used = models.BooleanField(default=False)  # 쿠폰 사용 여부
    created_at = models.DateTimeField(auto_now_add=True)  # 쿠폰 발급 일시

    def __str__(self):
        return f"{self.user.username} - {self.coupon.code}"