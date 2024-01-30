from django.db import models
from users.models import User
from restaurant.models import Restaurant

# Create your models here.
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user + self.restaurant  
