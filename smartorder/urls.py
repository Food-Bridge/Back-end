"""
URL configuration for smartorder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

# 문서화 drf_yasg
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="스마트오더 API",
        default_version='v1',
        description="백엔드 API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    ##### 메인 페이지
    path('users/', include('users.api.urls')),

    ##### 가게/가게 메뉴 페이지
    path('restaurant/', include('restaurant.api.urls')),
    path('restaurant/<int:res_id>/menu/', include('menu.api.urls')),

    ##### 쿠폰 페이지
    path('coupon/', include('coupon.api.urls')),
    
    ##### 검색
    path('search/', include('search.api.urls')),
    
    ##### 주문
    path('order/', include('order.api.urls')),

    ##### 커뮤니티 페이지
    path('community/', include('community.api.urls')),

    ##### 찜 목록 페이지
    path('like/', include('like.api.urls')),
  
    ##### 장바구니
    path('cart/', include('cart.api.urls')),

    ##### 주문내역 리뷰
    path('review/', include('review.api.urls')),

    ##### 유저가 보유하고 있는 쿠폰
    path('userscoupon/', include('users_coupon.api.urls')),
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
    ]