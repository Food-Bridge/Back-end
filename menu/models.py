from django.db import models
from restaurant.models import Restaurant
from django.core.validators import MaxValueValidator

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    content = models.CharField(max_length=150, blank=True, null=True) # 메뉴 상세 내용
    image = models.ImageField(upload_to='restaurant_image/menu/%Y/%m/%d', blank=True, null=True)
    is_main = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class MenuOption(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    is_required = models.BooleanField(default=False)
    
    BUTTON_TYPE = [
        ('option', 'Option'), 
        ('radio', 'Radio')
    ]
    
    type = models.CharField(max_length=10, choices=BUTTON_TYPE, default='option')

    def __str__(self):
        return self.name
