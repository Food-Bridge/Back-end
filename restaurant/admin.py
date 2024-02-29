from django.contrib import admin
from restaurant.models import Restaurant, MainCategory, SubCategory

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(MainCategory)
admin.site.register(SubCategory)