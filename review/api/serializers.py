from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from order.models import Order
from review.models import Review, ReviewImage, OwnerComment

class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ("id", "image",)

class OwnerCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerComment
        fields = ("id", "comments", "created", "review_id")

class ReviewSerializer(serializers.ModelSerializer):
    image = ReviewImageSerializer(many=True, source='img', read_only=True)
    review_written = serializers.BooleanField(source='order.review_written', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'user', 'restaurant', 'order', 'caption', 'menu_name',
                  'rating', 'created_at', 'like_count', 'image', 'review_written',)

class ReviewCreateSerializer(serializers.ModelSerializer):
    _img = ReviewImageSerializer(many=True, source="img", read_only=True)
    img = serializers.ListField(child=serializers.ImageField(), write_only=True, allow_null=True)

    class Meta:
        model = Review
        fields = ("id", "user", "restaurant", "order", "caption", "rating", "created_at", "menu_name", "img", "_img")
        read_only_fields = ("user", "restaurant", "order",)
        examples = {
            'id': 1,
            'taste': 4,
            'amount': 3,
            'delivery': 5,
            'restaurant': 2,
            'caption': '정말 맛이 없는걸!',
            'menu_name': '양념치킨',
        }

    def create(self, validated_data):
        images = validated_data.pop('img', None)
        review = Review.objects.create(**validated_data)
        if images:
            for image in images:
                ReviewImage.objects.create(review=review, image=image)
        return review