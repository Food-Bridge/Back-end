from django.urls import path
from order.api.views import OrderAPIView, OrderDetailAPIView

urlpatterns = [
    path('', OrderAPIView.as_view(), name="order"),
    path('<int:pk>', OrderDetailAPIView.as_view(), name="orderDetail"),
]