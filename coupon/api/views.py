from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from coupon.models import Coupon
from coupon.api.serializers import CouponSerializer

# Create your views here.
class CouponAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        coupons = Coupon.objects.all()
        serializer = CouponSerializer(coupons, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = CouponSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)