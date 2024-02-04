from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number_regex = RegexValidator(regex=r'^02?-?\d{3,4}-?\d{4}$')
    phone_number= models.CharField(validators = [phone_number_regex], max_length =13, unique=True)
    image = models.ImageField(upload_to='restaurant_image', blank=True, null=True)
    description = models.CharField(max_length=255, blank=True)
    minimumOrderPrice = models.IntegerField()
    minDeliveryTime = models.TimeField(null=True)
    maxDeliveryTime = models.TimeField(null=True)
    orderCount = models.IntegerField(default=0)
    reviewCouunt = models.IntegerField(default=0)
    bookmarkCount = models.IntegerField(default=0)
    rating = models.FloatField(validators=[MinValueValidator(0, 5), MaxValueValidator(5.0)])
    packaging = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    start = models.IntegerField(default=0)
    end = models.IntegerField(default=0)
    operatingTime = models.CharField(max_length=255)

    def __str__(self):
        return self.name