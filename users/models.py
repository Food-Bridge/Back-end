from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator
from rest_framework_simplejwt.tokens import RefreshToken

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
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_pn = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    phone_number_regex = RegexValidator(regex=r'^01[016789]?-?\d{3,4}-?\d{4}$')
    phone_number= models.CharField(validators = [phone_number_regex], max_length =13, unique=True)
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