from django.urls import path
from order.api.views import (OrderAPIView, 
                             OrderDetailAPIView,
                             OrderHistoryAPIView,
                             RetrieveReviewAPIView,
                             CompletedOrderReviewAPIView)

urlpatterns = [
    path('', OrderAPIView.as_view(), name="order"),
    path('<int:pk>', OrderDetailAPIView.as_view(), name="orderDetail"),
    path('history/', OrderHistoryAPIView.as_view(), name="orderHistory"),
    path('history/<int:pk>/', CompletedOrderReviewAPIView.as_view(), name="completedOrderReview"),
    path('review/', RetrieveReviewAPIView.as_view(), name="retrieve"),
]