from django.shortcuts import render
from rest_framework.views import APIView
from restaurant.api.serializers import RestaurantSerializer
from restaurant.models import Restaurant
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

# Create your views here.
class RestaurantAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, *args, **kwargs):
        restaurant = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurant, many=True)
        return Response(serializer.data)
    def post(self, request, *args, **kwargs):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)