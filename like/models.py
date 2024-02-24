from django.db import models
from users.models import User
from restaurant.models import Restaurant

# Create your models here.
class RestaurantLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    
    ##### rating(별점 책정)