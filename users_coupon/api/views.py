from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from users_coupon.api.serializers import UserCouponSerializer
from users_coupon.models import UserCoupon
from coupon.models import Coupon

# Create your views here.
class UserCouponAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # 혹은 필요에 따라 다른 권한을 사용

    def get_queryset(self):
        user_id = self.request.user.id
        return UserCoupon.objects.filter(user_id=user_id)

    def get(self, request, *args, **kwargs):
        user_coupons = self.get_queryset()
        serializer = UserCouponSerializer(user_coupons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)