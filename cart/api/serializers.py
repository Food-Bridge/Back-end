from rest_framework import serializers
from cart.models import cart
from menu.models import Menu


class CartSerializer(serializers.ModelSerializer):
    menu_image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = cart
        fields = "__all__"

    def get_menu_image(self, obj):
        menu_image_list = {}
        request = self.context.get('request')
        
        if not request:
            return {}
        
        for cart_menu in obj.cart_list:
            menu_id = cart_menu['menu_id']
            try:
                menu_data = Menu.objects.filter(id=menu_id).first()
                menu_image_list[cart_menu['menu_id']] = request.build_absolute_uri(menu_data.image.url)
            except Menu.DoesNotExist:
                pass
            except Menu.MultipleObjectsReturned:
                pass
        return menu_image_list