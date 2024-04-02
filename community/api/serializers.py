from rest_framework import serializers
from ..models import Blog, Comment, BlogImage
from users.models import User
from django.conf import settings

##### 사용자 정보 시리얼라이저
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', )

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ("id", "image",)

##### POST 요청(게시글 생성) 시리얼라이저 - 요구사항 반영
class PostCreateUpdateSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.id")
    _img = PostImageSerializer(many=True, source='img', read_only=True)
    img = serializers.ListField(child=serializers.ImageField(), write_only=True, allow_null=True, required=False)

    class Meta:
        model = Blog
        fields = ('author', 'title', 'content', 'created_at', 'updated_at', 'img', '_img')
        read_only_fields = ("author",)

    ##### 검증
    def validate_title(self, value):
        if len(value) == 0:
            return serializers.ValidationError("제목을 입력하지 않았습니다.")
        return value

    ##### 검증
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

##### GET 요청(전체 게시글 조회) 시리얼라이저 - 요구사항 반영
class PostListSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField(read_only=True)
    weight_value = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Blog
        fields = "__all__"

    def get_likes_count(self, obj):
        return obj.like_users.count()

    def get_weight_value(self, obj):
        return obj.WeightMethod()

##### GET/PUT/DELETE 요청(상세 보기 조회, 수정, 삭제) 시리얼라이저 - 요구사항 반영
class PostDetailSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField(read_only=True)
    like_users = serializers.SerializerMethodField(read_only=True)
    comment_count = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField()
    author = serializers.ReadOnlyField(source="author.id")

    class Meta:
        model = Blog
        fields = ('author', 'title', 'content', 'created_at', 'updated_at', 'like_users', 'comment_count', 'views', 'likes_count', 'image', 'id',)
    
    def get_likes_count(self, obj):
        return obj.like_users.count()
    
    def get_like_users(self, obj):
        like_users = obj.like_users.all()
        return UserInfoSerializer(like_users, many=True).data

    def get_comment_count(self, obj):
        return obj.comment.count()  # 해당 게시물의 댓글 수 반환

    def get_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url)


##### GET 요청(특정 게시물에 대한 모든 댓글 조회) 시리얼라이저 - 요구사항 반영
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.id")
    post = serializers.ReadOnlyField(source="post.id")
    id = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ("author", "id", "post", "content")

##### POST 요청(댓글 달기) 시리얼라이저 
class CommentCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ("content", )

##### GET/PUT/DELETE 요청(댓글 상세 조회, 수정, 삭제) 시리얼라이저
class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    post = serializers.ReadOnlyField(source="post.id")
    id = serializers.ReadOnlyField()
    class Meta:
        model = Comment
        fields = ('content', "id", "post",)

##### 좋아요 시리얼라이저
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

##### 인기 게시글 시리얼라이저
class PopularPostSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = "__all__"

    def get_comment_count(self, obj):
        return obj.comment.count()