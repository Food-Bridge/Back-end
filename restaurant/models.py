from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator

class MainCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "대분류"
        verbose_name_plural = "대분류"
        
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "중분류"
        verbose_name_plural = "중분류"
        
    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number_regex = RegexValidator(regex=r'^02?-?\d{3,4}-?\d{4}$')
    phone_number= models.CharField(validators = [phone_number_regex], max_length =13, unique=True)
    image = models.ImageField(default='default_restaurant.png', upload_to='restaurant_image/%Y/%m/%d', blank=True, null=True)
    description = models.CharField(max_length=255, blank=True)
    minimumOrderPrice = models.IntegerField()
    minDeliveryTime = models.TimeField(null=True)
    maxDeliveryTime = models.TimeField(null=True)
    orderCount = models.IntegerField(default=0)
    reviewCount = models.IntegerField(default=0)
    bookmarkCount = models.IntegerField(default=0)
    rating = models.FloatField(default=0, validators=[MinValueValidator(0, 5), MaxValueValidator(5.0)])
    packaging = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    start = models.IntegerField(default=0)
    end = models.IntegerField(default=0)
    operatingTime = models.CharField(max_length=255)
    delivertyFee = models.PositiveIntegerField(default=0)
    mainCategory = models.ForeignKey(
        MainCategory,
        on_delete=models.SET_DEFAULT,
        related_name='mainCategory',
        blank=True,
        default=None,
    )
    subCategory = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        related_name='subCategory',
        blank=True,
        null=True,
    )
    
    class Meta:
        verbose_name = "음식점"
        verbose_name_plural = "음식점"

    def __str__(self):
        return self.name