from django.urls import path
from users_coupon.api.views import UserCouponAPIView

urlpatterns = [
    path('', UserCouponAPIView.as_view(), name="usercoupon")
]