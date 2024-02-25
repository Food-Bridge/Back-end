from rest_framework import serializers
from menu.models import Menu, MenuOption

class MenuOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuOption
        fields = "__all__"

class MenuSerializer(serializers.ModelSerializer):
    options = MenuOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = "__all__"
