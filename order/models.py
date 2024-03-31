from django.db import models
from users.models import User
from restaurant.models import Restaurant
from menu.models import Menu
from coupon.models import Coupon
from django.core.validators import MinValueValidator, MaxValueValidator

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    review_written = models.BooleanField(default=False)
    
    coupon_code = models.ForeignKey(Coupon, blank=True, null=True, on_delete=models.SET_NULL)
    order_id = models.CharField(blank=True, null=True, max_length=50) # 주문 번호
    menu_list = models.JSONField(blank=True, default=dict) # 메뉴
    option_list = models.JSONField(blank=True, null=True) # 옵션
    soption_list = models.JSONField(blank=True, null=True) # 선택 옵션
    
    total_price = models.PositiveIntegerField(default=0)  # 주문의 총 가격
    deliveryman_request = models.TextField(blank=True, null=True) # 배송기사 요청
    required_options_count = models.PositiveIntegerField(default=1) # 필수 메뉴 개수
    
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', '신용 카드'),
        ('cash', '현금'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    
    deliver_address = models.CharField(blank=True, null=True, max_length=200)
    is_deliver = models.BooleanField(default=True)
    
    DELIVERY_IN_STATE = [
        ('waiting', "대기"),
        ('pickup_complete', "포장완료"),
        ('delivery_complete', "배달완료")
    ]
    
    delivery_state = models.CharField(
        default="대기",
        choices=DELIVERY_IN_STATE,
        verbose_name="포장배달 상태",
        max_length=20
    )
    
    STATE_IN_ORDER = [
        ('order_complete', '주문완료'),
        ('payment_complete', '결제완료'),
        ('order_cancel', '주문취소'),
        ('payment_cancel', '결제취소'),
    ]
    
    order_state = models.CharField(
        default="주문완료",
        choices=STATE_IN_ORDER,
        verbose_name="주문서 상태",
        max_length=16
    )

    # DecimalField
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
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)