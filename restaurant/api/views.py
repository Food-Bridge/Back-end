from restaurant.api.serializers import RestaurantSerializer
from restaurant.models import Restaurant
from rest_framework import permissions, generics, status
from rest_framework.response import Response

class RestaurantAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    
    def create(self, request, *args, **kwargs):
        # 유저가 판매자인지 여부 확인
        if request.user.is_authenticated and request.user.is_seller:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Only sellers can create restaurants."}, status=status.HTTP_200_OK)

class RestaurantDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()