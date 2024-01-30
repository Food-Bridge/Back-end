from django.db import models
from restaurant.models import Restaurant
from category.models import Category
from django.core.validators import MaxValueValidator

class Menu(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    rating = models.FloatField()
    image = models.ImageField(upload_to='menu/')
    is_main = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class MenuOption(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    is_checked = models.BooleanField(default=False)
    check_option = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(3)])

    def __str__(self):
        return self.name
