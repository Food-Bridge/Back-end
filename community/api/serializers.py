from rest_framework import serializers
from ..models import Blog, Comment, BlogImage
from users.models import Profile
from users.models import User

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', )

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ("id", "image",)

class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('user', 'nickname', 'image')

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url)
        else:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image_original.url)

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    author_info = ProfileSerializer(source="author.profile", read_only=True)
    author = serializers.ReadOnlyField(source="author.id", read_only=True)
    _img = PostImageSerializer(many=True, source='img', read_only=True)
    img = serializers.ListField(child=serializers.ImageField(), write_only=True, allow_null=True, required=False)

    class Meta:
        model = Blog
        fields = ('author', 'title', 'content', 'created_at', 'updated_at', 'img', '_img', "author_info",)
        read_only_fields = ("author", "author_info",)

    def validate_title(self, value):
        if len(value) == 0:
            return serializers.ValidationError("제목을 입력하지 않았습니다.")
        return value

    def validate_content(self, value):
        if len(value) == 0:
            return serializers.ValidationError("내용을 입력하지 않았습니다.")
        return value

    def create(self, validated_data):
        images = validated_data.pop('img', None)
        post = Blog.objects.create(**validated_data)
        if images:
            for image in images:
                BlogImage.objects.create(blog=post, image=image)
        return post

class PostListSerializer(serializers.ModelSerializer):
    author_info = ProfileSerializer(source="author.profile", read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    weight_value = serializers.SerializerMethodField(read_only=True)
    img = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = ("author", "title", "content", "created_at", "updated_at", "views", "img", "likes_count", "weight_value", "author_info",)

    def get_likes_count(self, obj):
        return obj.like_users.count()

    def get_weight_value(self, obj):
        return obj.WeightMethod()
    
    def get_img(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.img.url)

class PostDetailSerializer(serializers.ModelSerializer):
    author_info = ProfileSerializer(source="author.profile", read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    like_users = serializers.SerializerMethodField(read_only=True)
    comment_count = serializers.SerializerMethodField(read_only=True)
    image = PostImageSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source="author.id")

    class Meta:
        model = Blog
        fields = ('author', 'title', 'content', 'created_at', 'updated_at', 'like_users', 'comment_count', 'views', 'likes_count', 'image', 'id', "author_info",)
    
    def get_likes_count(self, obj):
        return obj.like_users.count()
    
    def get_like_users(self, obj):
        like_users = obj.like_users.all()
        return UserInfoSerializer(like_users, many=True).data

    def get_comment_count(self, obj):
        return obj.comment.count()

    def get_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url)

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.id")
    post = serializers.ReadOnlyField(source="post.id")
    id = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ("author", "id", "post", "content",)

class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    post = serializers.ReadOnlyField(source="post.id")
    id = serializers.ReadOnlyField()
    class Meta:
        model = Comment
        fields = ('content', "id", "post",)

class PostLikeSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    like_users = serializers.SerializerMethodField(read_only=True)

    def get_email(self, obj):
        return obj.author.email
    
    def get_likes_count(self, obj):
        return obj.like_users.count()

    class Meta:
        model = Blog
        fields = ('id', 'email', 'like_users', 'likes_count',)

class PopularPostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField(read_only=True)
    comment_count = serializers.SerializerMethodField()
    img = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = ("author", "title", "content", "created_at", "updated_at", "views", "img", "comment_count", "likes_count",)

    def get_likes_count(self, obj):
        return obj.like_users.count()

    def get_comment_count(self, obj):
        return obj.get_comment_count()
    
    def get_img(self, obj):
        return obj.image.url