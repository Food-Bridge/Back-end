from rest_framework import serializers
from ..models import Post, Comment, PostImage
from users.api.serializers import ProfileSerializer

class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImage
        fields = ('id', 
                  'image',)

class CommenterSerializer(serializers.ModelSerializer):
    author_profile = ProfileSerializer(source='author.profile', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 
                  'content', 
                  'author_profile')


class PostCreateUpdateSerializer(serializers.ModelSerializer):

    author_info = ProfileSerializer(source="author.profile", read_only=True)
    author = serializers.ReadOnlyField(source="author.id", read_only=True)
    _img = PostImageSerializer(many=True, source='img', read_only=True)
    img = serializers.ListField(child=serializers.ImageField(), write_only=True, allow_null=True, required=False)

    class Meta:
        model = Post
        fields = ('author', 
                  'title', 
                  'content', 
                  'created_at',
                  'updated_at', 
                  'img', 
                  '_img', 
                  "author_info",)

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
        post = Post.objects.create(**validated_data)
        if images:
            for image in images:
                PostImage.objects.create(post=post, image=image)
        return post


class PostListSerializer(serializers.ModelSerializer):

    author_info = ProfileSerializer(source="author.profile", read_only=True)
    likes_count = serializers.IntegerField(source='like_users.count', read_only=True)
    weight_value = serializers.IntegerField(source='standard_method', read_only=True)
    _img = PostImageSerializer(many=True, source='img', read_only=True)   
    img = serializers.ListField(child=serializers.ImageField(), write_only=True, allow_null=True, required=False)

    class Meta:
        model = Post
        fields = ("id", 
                  "author", 
                  "title",
                  "content", 
                  "created_at", 
                  "updated_at",
                  "_img",
                  "img", 
                  "likes_count", 
                  "weight_value", 
                  "author_info",)

    def get_img(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.img.url)

class PostDetailSerializer(serializers.ModelSerializer):

    author_info = ProfileSerializer(source="author.profile", read_only=True)
    likes_count = serializers.IntegerField(source='like_users.count', read_only=True)
    like_users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comment.count', read_only=True)
    _img = PostImageSerializer(many=True, source='img', read_only=True, allow_null=True)
    img = serializers.ListField(child=serializers.ImageField(), write_only=True, allow_null=True, required=False)
    comments = CommenterSerializer(many=True, source='comment.all', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 
                  'title', 
                  'content', 
                  'created_at', 
                  'updated_at', 
                  'like_users', 
                  'comment_count', 
                  'likes_count', 
                  'author_info',
                  'img', 
                  '_img', 
                  'comment_count', 
                  'comments',)

    def get_img(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.img.url)

class CommentSerializer(serializers.ModelSerializer):

    author_info = ProfileSerializer(source="user.profile", write_only=True)
    author = serializers.ReadOnlyField(source="author.id", read_only=True)
    post = serializers.ReadOnlyField(source="post.id")

    class Meta:
        model = Comment
        fields = ('id', 
                  'post', 
                  'content', 
                  'author', 
                  'author_info')

class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    post = serializers.ReadOnlyField(source="post.id")

    class Meta:
        model = Comment
        fields = ('id', 
                  'content',
                  'post')

class PostLikeSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(source='author.email', read_only=True)
    likes_count = serializers.IntegerField(source='like_users.count', read_only=True)
    like_users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 
                  'email', 
                  'like_users', 
                  'likes_count',)