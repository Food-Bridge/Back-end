from rest_framework import serializers
from menu.models import Menu, MenuOption, MenuSelectedOption


class MenuSelectedOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuSelectedOption
        fields = "__all__"

class MenuOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuOption
        fields = "__all__"

class MenuSerializer(serializers.ModelSerializer):
    options = MenuOptionSerializer(many=True, read_only=True)
    select_options = MenuSelectedOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = "__all__"
        read_only_fields = ('restaurant',)

