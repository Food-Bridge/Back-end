from django.contrib import admin
from .models import Menu, MenuOption, MenuSelectedOption

# Register your models here.
admin.site.register(Menu)
admin.site.register(MenuOption)
admin.site.register(MenuSelectedOption)
