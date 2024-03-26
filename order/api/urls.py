from django.urls import path
from order.api.views import OrderAPIView, OrderDetailAPIView, GetKakaoMobilityView

urlpatterns = [
    path('', OrderAPIView.as_view(), name="order"),
    path('<int:pk>', OrderDetailAPIView.as_view(), name="orderDetail"),
    path('estimate/<int:order_id>', GetKakaoMobilityView.as_view(), name="estimate")
]