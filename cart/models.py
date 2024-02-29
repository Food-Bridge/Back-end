from django.db import models
from users.models import User
import json

class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_id = models.PositiveIntegerField(null=True)
    food_name = models.CharField(max_length=100)
    food_price = models.IntegerField(null=True)
    amount = models.IntegerField(null=True)
    total_price = models.PositiveIntegerField(default=0)
    option_name = models.JSONField(default=dict, null=True)
    option_price = models.JSONField(default=dict, null=True)
    restaurant_id = models.PositiveIntegerField(null=True)

    def deserialize_json_fields(self):
        # JSONField에서 객체를 가져오기 위해 역직렬화
        self.option_name = json.loads(self.option_name)
        self.option_price = json.loads(self.option_price)
        self.option_id = json.loads(self.option_id)
    
    def calculate_total_price(self):
        option_total_price = sum(self.option_price.values())
        food_price = self.food_price or 0 # 예외처리
        amount = self.amount or 0 # 예외처리
        self.total_price = option_total_price + (food_price * amount)
    
    def save(self, *args, **kwargs):
        self.calculate_total_price()  # total_price 계산
        super().save(*args, **kwargs)  # 부모 클래스의 save 메서드 호출하여 저장
