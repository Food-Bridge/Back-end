from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from menu.models import Menu, MenuOption, MenuSelectedOption
from restaurant.models import Restaurant
from menu.api.serializers import MenuSerializer, MenuOptionSerializer, MenuSelectedOptionSerializer

class MenuListCreateAPIView(generics.ListCreateAPIView):
    """
    레스토랑 ID에 따른 메뉴 조회, 생성 API
    """
    permission_classes = [permissions.AllowAny] 
    serializer_class = MenuSerializer

    def get_queryset(self):
        res_id = self.kwargs.get('res_id')  # URL에서 'res_id' 가져오기
        
        get_object_or_404(Restaurant, pk=res_id)
        
        return Menu.objects.filter(restaurant_id=res_id)
    
    def perform_create(self, serializer):
        res_id = self.kwargs.get('res_id')
        restaurant = get_object_or_404(Restaurant, pk=res_id)
        serializer.save(restaurant=restaurant)
        
class MenuRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    레스토랑 ID와 메뉴 ID 활용하여 조회, 수정, 삭제 API
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = MenuSerializer
    lookup_url_kwarg = 'menu_id'
    
    def get_queryset(self):
        res_id = self.kwargs.get('res_id')  # URL에서 'res_id' 가져오기
        menu_id = self.kwargs.get('menu_id') # URL에서 'menu_id' 가져오기
        
        get_object_or_404(Restaurant, pk=res_id)
        get_object_or_404(Menu, pk=menu_id)
        
        return Menu.objects.filter(id=menu_id)
    

class MenuOptionListCreateAPIView(generics.ListCreateAPIView):
    """
    레스토랑 ID와 메뉴 ID 활용하여 옵션 조회, 생성 API
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = MenuOptionSerializer
    
    def get_queryset(self):
        res_id = self.kwargs.get('res_id')  # URL에서 'res_id' 가져오기
        menu_id = self.kwargs.get('menu_id') # URL에서 'menu_id' 가져오기
        
        get_object_or_404(Restaurant, pk=res_id)
        get_object_or_404(Menu, pk=menu_id)
        
        return MenuOption.objects.filter(menu_id=menu_id)
    
    def perform_create(self, serializer):
        res_id = self.kwargs.get('res_id')  # URL에서 'res_id' 가져오기
        menu_id = self.kwargs.get('menu_id') # URL에서 'menu_id' 가져오기
        
        # 메뉴를 가져와서 옵션을 생성할 때 해당 메뉴와 연결
        menu = get_object_or_404(Menu, pk=menu_id)
        res = get_object_or_404(Restaurant, pk=res_id)
        
        serializer.save(menu=menu)

class MenuOptionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    레스토랑 ID와 메뉴 ID, 옵션 ID 활용하여 옵션 조회, 수정, 삭제 API
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = MenuOptionSerializer
    lookup_url_kwarg = 'option_id'
    
    def get_queryset(self):
        res_id = self.kwargs.get('res_id')  # URL에서 'res_id' 가져오기
        menu_id = self.kwargs.get('menu_id') # URL에서 'menu_id' 가져오기
        menu_option_id = self.kwargs.get('option_id') # URL에서 'option_id' 가져오기
        
        get_object_or_404(Restaurant, pk=res_id)
        get_object_or_404(Menu, pk=menu_id)
        get_object_or_404(MenuOption, pk=menu_option_id)
        
        return MenuOption.objects.filter(id=menu_option_id)

class MenuSOptionListCreateAPIView(generics.ListCreateAPIView):
    """
    레스토랑 ID와 메뉴 ID 활용하여 옵션 조회, 생성 API
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = MenuSelectedOptionSerializer
    
    def get_queryset(self):
        res_id = self.kwargs.get('res_id')  # URL에서 'res_id' 가져오기
        menu_id = self.kwargs.get('menu_id') # URL에서 'menu_id' 가져오기
        
        get_object_or_404(Restaurant, pk=res_id)
        get_object_or_404(Menu, pk=menu_id)
        
        return MenuSelectedOption.objects.filter(menu_id=menu_id)
    
    def perform_create(self, serializer):
        res_id = self.kwargs.get('res_id')  # URL에서 'res_id' 가져오기
        menu_id = self.kwargs.get('menu_id') # URL에서 'menu_id' 가져오기
        
        # 메뉴를 가져와서 옵션을 생성할 때 해당 메뉴와 연결
        menu = get_object_or_404(Menu, pk=menu_id)
        res = get_object_or_404(Restaurant, pk=res_id)
        
        serializer.save(menu=menu)
        
class MenuSOptionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    레스토랑 ID와 메뉴 ID, 옵션 ID 활용하여 옵션 조회, 수정, 삭제 API
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = MenuSelectedOptionSerializer
    lookup_url_kwarg = 'option_id'
    
    def get_queryset(self):
        res_id = self.kwargs.get('res_id')  # URL에서 'res_id' 가져오기
        menu_id = self.kwargs.get('menu_id') # URL에서 'menu_id' 가져오기
        menu_option_id = self.kwargs.get('option_id') # URL에서 'option_id' 가져오기
        
        get_object_or_404(Restaurant, pk=res_id)
        get_object_or_404(Menu, pk=menu_id)
        get_object_or_404(MenuSelectedOption, pk=menu_option_id)
        
        return MenuSelectedOption.objects.filter(id=menu_option_id)