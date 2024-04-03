from rest_framework import serializers

from review.models import Review, ReviewImage

class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ("id", "image",)

class ReviewSerializer(serializers.ModelSerializer):
    image = ReviewImageSerializer(many=True, source='img', read_only=True)
    review_written = serializers.BooleanField(source='order.review_written', read_only=True)
    user_nickname = serializers.CharField(source='user.profile.nickname', read_only=True)
    user_image = serializers.SerializerMethodField(source='user.profile', read_only=True)
    
    restaurant_name = serializers.SerializerMethodField()
    restaurant_image = serializers.SerializerMethodField()
    
    def get_user_image(self, obj):
        user = obj.user
        profile = user.profile
        request = self.context.get('request')

        if profile.image_original and request:
            return request.build_absolute_uri(profile.image_original.url)
        elif profile.image and request:
            return request.build_absolute_uri(profile.image.url)
        else:
            return None
    
    def get_restaurant_name(self, obj):
        res = obj.restaurant
        return res.name
    
    def get_restaurant_image(self, obj):
        request = self.context.get('request')
        res = obj.restaurant
        return request.build_absolute_uri(res.image.url)
    
    class Meta:
        model = Review
        fields = ('id', 'user', 'user_nickname', 'user_image', 'restaurant', 'restaurant_name', 'restaurant_image',
                  'order', 'caption', 'menu_name','rating', 'created_at', 'like_count', 'image', 'review_written',)

class ReviewCreateSerializer(serializers.ModelSerializer):
    _img = ReviewImageSerializer(many=True, source="img", read_only=True)
    img = serializers.ListField(child=serializers.ImageField(), write_only=True, allow_null=True, required=False)
    caption = serializers.CharField()
    rating = serializers.DecimalField(max_digits=2, decimal_places=1)

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