from django.urls import path
from coupon.api.views import CouponAPIView

urlpatterns = [
    path('', CouponAPIView.as_view(), name="coupon")
]