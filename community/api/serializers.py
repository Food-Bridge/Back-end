from rest_framework import serializers
from ..models import Post, Comment, PostImage
from users.models import User
from users.api.serializers import ProfileSerializer


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', )


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ("id", "image",)

class CommenterSerializer(serializers.ModelSerializer):
    author_profile = ProfileSerializer(source='author.profile', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'created_at', 'author_profile')


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    author_info = ProfileSerializer(source="author.profile", read_only=True)
    author = serializers.ReadOnlyField(source="author.id", read_only=True)
    _img = PostImageSerializer(many=True, source='img', read_only=True)
    img = serializers.ListField(child=serializers.ImageField(
    ), write_only=True, allow_null=True, required=False)

    class Meta:
        model = Post
        fields = ('author', 'title', 'content', 'created_at',
                  'updated_at', 'img', '_img', "author_info",)
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
        post = Post.objects.create(**validated_data)
        if images:
            for image in images:
                PostImage.objects.create(blog=post, image=image)
        return post


class PostListSerializer(serializers.ModelSerializer):
    author_info = ProfileSerializer(source="author.profile", read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    weight_value = serializers.SerializerMethodField(read_only=True)
    img = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("id", "author", "title", "content", "created_at", "updated_at",
                  "views", "img", "likes_count", "weight_value", "author_info",)

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
    _img = PostImageSerializer(many=True, source='img', read_only=True)
    img = serializers.ListField(
        child=serializers.ImageField(), write_only=True, allow_null=True)
    comment_count = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'like_users', 'comment_count', 'views', 'likes_count', 'id', "author_info",
                  "img", "_img", "comment_count", "comments",)

    def get_likes_count(self, obj):
        return obj.like_users.count()

    def get_like_users(self, obj):
        like_users = obj.like_users.all()
        return UserInfoSerializer(like_users, many=True).data

    def get_comment_count(self, obj):
        return obj.comment.count()

    def get_img(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.img.url)

    def get_comments(self, obj):
        comments = obj.comment.all()
        return CommentSerializer(comments, many=True).data


class CommentSerializer(serializers.ModelSerializer):
    # 4/13 댓글 작성자 닉네임 필드 추가 필요()
    author_info = ProfileSerializer(source="user.profile", write_only=True)

    #  4/13 코드 확인 필요()
    # author = serializers.ReadOnlyField(source="user.id")
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    post = serializers.ReadOnlyField(source="post.id")
    id = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ("id", "post", "content", "author", "author_info")


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    post = serializers.ReadOnlyField(source="post.id")
    id = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ('content', "id", "post")


class PostLikeSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    like_users = serializers.SerializerMethodField(read_only=True)

    def get_email(self, obj):
        return obj.author.email

    def get_likes_count(self, obj):
        return obj.like_users.count()

    class Meta:
        model = Post
        fields = ('id', 'email', 'like_users', 'likes_count',)


class PopularPostSerializer(serializers.ModelSerializer):
    author_info = ProfileSerializer(source="author.profile", read_only=True)
    author = serializers.ReadOnlyField(source="author.id", read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    comment_count = serializers.SerializerMethodField()
    img = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("id", "author", "title", "content", "created_at", "updated_at",
                  "views", "img", "comment_count", "likes_count", "author_info",)

    def get_likes_count(self, obj):
        return obj.like_users.count()

    def get_comment_count(self, obj):
        return obj.get_comment_count()

    def get_img(self, obj):
        return obj.image.url
