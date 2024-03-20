from django.shortcuts import get_object_or_404
from order.models import Order
from review.models import Review, OwnerComment
from review.api.serializers import ReviewSerializer, ReviewCreateSerializer, OwnerCommentSerializer
from rest_framework import permissions, generics, status, serializers, response
from rest_framework.response import Response

class ReviewCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_order(self):
        user = self.request.user
        order_pk = self.kwargs.get('order_pk')
        order = get_object_or_404(Order, id=order_pk)
        return order

    def perform_create(self, serializer):
        order = self.get_order()
        user = self.request.user  # 현재 요청의 사용자를 가져옵니다.
        serializer.save(restaurant=order.restaurant, order=order, user=user)

class ReviewListAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        reviews = Review.objects.filter(user=user).order_by("created_at")
        serializer = self.serializer_class(reviews, many=True)
        return Response(serializer.data)
