from django.db import models
from django.db.models import F
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator 
from users.models import User
from restaurant.models import Restaurant
from order.models import Order
from decimal import Decimal

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="review")
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, related_name="review", null=True)
    caption = models.CharField(max_length=300, default="")
    menu_name = models.CharField(max_length=100, default="")
    rating = models.DecimalField(decimal_places=1, max_digits=2, validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-id"]
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            self.restaurant = self.order.restaurant
            super().save(force_insert, force_update, using, update_fields)
            """리뷰 생성 시 해당 주문 내역에 대한 review_written -> True"""
            """별점 계산 : """
            self.order.review_written = True
            self.order.save()

            self.restaurant.reviewCount += 1
            self.restaurant.save()
        
        # 예외 처리(맨 처음 상태)
        if self.restaurant.reviewCount == 0:
            self.restaurant.averageRating = Decimal('0.00')
        else:
            self.restaurant.averageRating = Decimal(self.restaurant.averageRating * (self.restaurant.reviewCount - 1) + self.rating) / Decimal(self.restaurant.reviewCount)
            self.restaurant.save()


class ReviewImage(models.Model):
    """이미지 모델"""
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="img")
    image = models.ImageField(upload_to="review_image")

class OwnerComment(models.Model):
    review = models.OneToOneField(Review, on_delete=models.CASCADE)
    comments = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)