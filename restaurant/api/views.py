import requests
from restaurant.api.serializers import RestaurantSerializer
from restaurant.models import Restaurant
from rest_framework import permissions, generics, status
from rest_framework.response import Response

from django.conf import settings
from urllib.parse import urlparse

class RestaurantAPIView(generics.ListCreateAPIView):
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
                        geocoded_data = self.geocode_address(address)
                        if geocoded_data:
                            data.update(geocoded_data)
                    except requests.exceptions.RequestException as e:
                        return Response({'error': f"Error during geocoding: {e}"}, status=status.HTTP_400_BAD_REQUEST)
                serializer.save(**data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Only sellers can create restaurants."}, status=status.HTTP_200_OK)
        
    def geocode_address(self, address):
        KAKAO_REST_API_KEY = getattr(settings, 'KAKAO_REST_API_KEY')
        url = f"https://dapi.kakao.com/v2/local/search/address.json?query={address}"
        
        try:
            response = requests.get(urlparse(url).geturl(), headers={"Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"})
            if response.status_code == 200:
                result = response.json()
                documents = result.get('documents', [])
                if documents:
                    return {
                        'latitude': float(documents[0]['y']),
                        'longitude': float(documents[0]['x']),
                    }
        except requests.exceptions.RequestException as e:
            raise Response({'error': f"Error during geocoding: {e}"}, status=status.HTTP_400_BAD_REQUEST)
        
class RestaurantDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()