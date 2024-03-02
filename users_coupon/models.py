from django.db import models
from restaurant.models import Restaurant
from coupon.models import Coupon
from users.models import User

# Create your models here.
class UserCoupon(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)