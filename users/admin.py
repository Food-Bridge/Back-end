from django.contrib import admin
from .models import User, Address, Order, Profile

# 유저 모델과 프로파일 모델을 함께 등록
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(Order)