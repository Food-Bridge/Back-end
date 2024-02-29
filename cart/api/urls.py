from django.urls import path
from cart.api import views

urlpatterns = [
     path('', views.CartAPIView.as_view(), name='cart-list'),
]