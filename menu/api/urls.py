from django.urls import path
from menu.api import views

urlpatterns = [
    path('', views.MenuListCreateAPIView.as_view(), name='menu-list-create'),
    path('<int:menu_id>/', views.MenuRetrieveUpdateDestroyAPIView.as_view(), name='menu-detail'),
    path('<int:menu_id>/options/', views.MenuOptionListCreateAPIView.as_view(), name='menu-option-list-create'),
    path('<int:menu_id>/options/<int:option_id>/', views.MenuOptionRetrieveUpdateDestroyAPIView.as_view(), name='menu-option-detail'),
]
