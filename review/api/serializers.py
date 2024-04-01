from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from order.models import Order
from users.models import Profile
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
    user_nickname = serializers.CharField(source='user.profile.nickname', read_only=True)
    user_image = serializers.SerializerMethodField()

    def get_user_image(self, obj):
        user = obj.user
        profile = user.profile
        if profile.image:
            return self.context['request'].build_absolute_uri(profile.image.url)
        else:
            return self.context['request'].build_absolute_uri(profile.image_original.url)

    class Meta:
        model = Review
        fields = ('id', 'user', 'user_nickname', 'user_image', 'restaurant', 'order', 'caption', 'menu_name',
                  'rating', 'created_at', 'like_count', 'image', 'review_written',)

class ReviewCreateSerializer(serializers.ModelSerializer):
    _img = ReviewImageSerializer(many=True, source="img", read_only=True)
    img = serializers.ListField(child=serializers.ImageField(), write_only=True, allow_null=True)
    caption = serializers.CharField()
    rating = serializers.IntegerField()

    class Meta:
        model = Review
        fields = ("id", "user", "restaurant", "order", "caption", "rating", "created_at", "menu_name", "img", "_img")
        read_only_fields = ("user", "restaurant", "order",)

    def validate_ratings(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("최소 1점 이상, 최대 5점 이하까지만 부여할 수 있습니다.")
        return value

    def create(self, validated_data):
        images = validated_data.pop('img', None)
        review = Review.objects.create(**validated_data)
        if images:
            for image in images:
                ReviewImage.objects.create(review=review, image=image)
        return review