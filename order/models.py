from django.db import models
from users.models import User
from restaurant.models import Restaurant
from menu.models import Menu

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    
    order_id = models.CharField(blank=True, null=True, max_length=50) # 주문 번호
    menu_list = models.JSONField(blank=True, default=dict) # 메뉴
    option_list = models.JSONField(blank=True, null=True) # 옵션
    
    total_price = models.PositiveIntegerField(default=0)  # 주문의 총 가격
    deliveryman_request = models.TextField(blank=True, null=True) # 배송기사 요청
    required_options_count = models.PositiveIntegerField(default=1) 
    
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', '신용 카드'),
        ('cash', '현금'),
    ]
    paymentMethod = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    
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
    created_at = models.DateTimeField(auto_now_add=True)