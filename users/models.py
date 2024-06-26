from django.conf import settings
from django.db import models, IntegrityError, transaction
from django.db.models import UniqueConstraint, Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from rest_framework_simplejwt.tokens import RefreshToken
from coupon.models import Coupon
from restaurant.models import Restaurant
from django_resized import ResizedImageField
import requests

from django.core.validators import MinValueValidator, MaxValueValidator

state = getattr(settings, "KAKAO_REST_API_KEY") 

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Please provide an email address")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email, 
            password=password,
            username=username,
        )
        user.is_admin=True
        user.save(using=self.db)
        return user
    
class User(AbstractBaseUser):
    coupons = models.ManyToManyField(Coupon)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number_regex = RegexValidator(regex=r'^01[016789]?-?\d{3,4}-?\d{4}$')
    phone_number= models.CharField(validators = [phone_number_regex], max_length =13, unique=False)
    is_seller   = models.BooleanField(
        verbose_name='판매자 여부',
        default=False
    )
    grade       = models.TextField(max_length=5, default='C')
    order_count = models.IntegerField(null=False, default=0)

    class Meta:
        db_table = 'users'
    
    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True


    def has_module_perms(self, app_label):
        return True

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_address = models.CharField(max_length=255, blank=True, null=True)
    detail_address = models.CharField(max_length=255, verbose_name='address')
    nickname = models.CharField(max_length=255, null=True, blank=True)
    building_name = models.CharField(max_length=255, null=True)
    road_address = models.CharField(max_length=255, blank=True, null=True)
    jibun_address = models.CharField(max_length=255, blank=True, null=True)
    sigungu = models.CharField(max_length=255, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    latitude = models.DecimalField(
        max_digits=15,
        decimal_places=11,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        null=True
    )
    longitude = models.DecimalField(
        max_digits=15,
        decimal_places=11,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        null=True
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'is_default'],
                condition=Q(is_default=True),
                name="한 유저당 하나의 주소만 기본 주소지로 등록되어야합니다."
            )
        ]

class Profile(models.Model):
    # primary_key를 User의 pk로 설정하여 통합 관리
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField(max_length=20)
    image = ResizedImageField(size=[500,500], upload_to="profile/resize/%Y/%m/%d" , null=True, blank=True)
    image_original = models.ImageField(upload_to='profile/%Y/%m/%d', default='default.png')
    

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)