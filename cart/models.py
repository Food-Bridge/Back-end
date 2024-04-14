from django.db import models
from users.models import User
from restaurant.models import Restaurant

class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    menu_list = models.JSONField(blank=True, default=dict) # 메뉴
    option_list = models.JSONField(blank=True, null=True) # 옵션
    soption_list = models.JSONField(blank=True, null=True) # 선택 옵션
    total_price = models.PositiveIntegerField(default=0)  # 주문의 총 가격
    created_at = models.DateTimeField(auto_now_add=True)
