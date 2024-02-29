from rest_framework import status
from rest_framework import views
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import LikeSerializer
from ..models import RestaurantLike

class LikeAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)  

    def get(self, request, *args, **kwargs):
        user = request.user
        # 해당 사용자가 좋아요한 모든 식당을 가져옴
        likes = RestaurantLike.objects.filter(user=user)
        # 각 좋아요에 있는 식당의 ID를 추출하여 리스트로 만듦
        liked_restaurants_ids = [like.restaurant_id for like in likes]
        return Response({'liked_restaurants_ids': liked_restaurants_ids}, status=status.HTTP_200_OK)

class LikeCreateAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)  

    def post(self, request, *args, **kwargs):
        user = request.user
        restaurant_id = kwargs.get('pk')  # kwargs에서 식당의 PK(ID)를 가져옴
        if restaurant_id:
            existing_like = RestaurantLike.objects.filter(user=user, restaurant_id=restaurant_id).first()
            if existing_like:
                # 이미 좋아요를 누른 경우 좋아요 취소
                existing_like.delete()
                return Response({'message': 'Restaurant like cancelled successfully.'}, status=status.HTTP_204_NO_CONTENT)
            else:
                # 좋아요 등록
                like = RestaurantLike(user=user, restaurant_id=restaurant_id)
                like.save()
                return Response({'message': 'Restaurant liked successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Restaurant ID is required.'}, status=status.HTTP_400_BAD_REQUEST)