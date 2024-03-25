import requests
from rest_framework import permissions, generics, status
from rest_framework.response import Response

from restaurant.api.serializers import RestaurantSerializer
from restaurant.models import Restaurant
from review.models import Review
from review.api.serializers import ReviewSerializer
from users.api.utils import geocode_address

class RestaurantAPIView(generics.ListCreateAPIView):
    """
    예시 데이터
    ```
    {
        "name": "string2",
        "address": "서울 관악구 난곡로 21길 10",
        "phone_number": "021334294",
        "description": "string",
        "minimumOrderPrice": 3000,
        "minimumPickupPrice": 3000,
        "minPickupTime": 30,
        "orderCount": 3000,
        "reviewCount": 3000,
        "bookmarkCount": 3000,
        "rating": 5,
        "packaging": true,
        "status": true,
        "start": 24,
        "end": 36,
        "operatingTime": "string",
        "deliveryFee": 3000,
        "mainCategory": 1,
        "subCategory": null
    }
    ```
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    
    def create(self, request, *args, **kwargs):
        # 유저가 판매자인지 여부 확인
        if request.user.is_authenticated and request.user.is_seller:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                address = data.get('address')
                if address:
                    try:
                        geocoded_data = geocode_address(address)
                        if geocoded_data:
                            data.update(geocoded_data)
                    except requests.exceptions.RequestException as e:
                        return Response({'error': f"Error during geocoding: {e}"}, status=status.HTTP_400_BAD_REQUEST)
                serializer.save(**data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Only sellers can create restaurants."}, status=status.HTTP_200_OK)
        
class RestaurantDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    
class RestaurantReviewAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        restaurant_id = self.kwargs.get('pk')
        return Review.objects.filter(restaurant_id=restaurant_id)