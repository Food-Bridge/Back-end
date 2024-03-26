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
    name = models.CharField(max_length=255, verbose_name="매장 이름")
    address = models.CharField(max_length=255, verbose_name="매장 주소")
    phone_number_regex = RegexValidator(regex=r'^02?-?\d{3,4}-?\d{4}$')
    phone_number= models.CharField(validators = [phone_number_regex], max_length =13, unique=True, verbose_name="매장 전화번호")
    image = models.ImageField(default='default_restaurant.png', upload_to='restaurant_image/%Y/%m/%d', blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, verbose_name="매장 설명")
    minimumOrderPrice = models.PositiveIntegerField(default=0, verbose_name="최소 주문 금액")
    minimumPickupPrice = models.PositiveIntegerField(default=0, verbose_name=" 픽업 최소 주문 금액")
    
    minDeliveryTime = models.PositiveSmallIntegerField(default=0, verbose_name="최소 배달 시간")
    maxDeliveryTime = models.PositiveSmallIntegerField(default=0, verbose_name="최대 배달 시간") 
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    minPickupTime = models.PositiveIntegerField(default=0, null=True, verbose_name="최소 픽업 시간")
    orderCount = models.PositiveIntegerField(default=0, verbose_name="주문수")
    reviewCount = models.PositiveIntegerField(default=0, verbose_name="리뷰수")
    bookmarkCount = models.PositiveIntegerField(default=0, verbose_name="즐겨찾기수")
    rating = models.FloatField(default=0, validators=[MinValueValidator(0, 5), MaxValueValidator(5.0)])
    packaging = models.BooleanField(default=False, verbose_name="포장 여부")
    status = models.BooleanField(default=False, verbose_name="매장 운영 여부")
    start = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0, 24), MaxValueValidator(24)], verbose_name="영업 시작 시간")
    end = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0, 36), MaxValueValidator(36)], verbose_name="영업 마감 시간")
    operatingTime = models.CharField(max_length=255, verbose_name="운영 시간 설명")
    deliveryFee = models.PositiveIntegerField(default=0, verbose_name="배달 요금")
    
    mainCategory = models.ForeignKey(
        MainCategory,
        on_delete=models.SET_DEFAULT,
        related_name='mainCategory',
        blank=True,
        default=None,
        verbose_name="매장 대분류"
    )
    subCategory = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        related_name='subCategory',
        blank=True,
        null=True,
        verbose_name="매장 중분류"
    )
    
    class Meta:
        verbose_name = "매장"
        verbose_name_plural = "매장"

    def __str__(self):
        return self.name