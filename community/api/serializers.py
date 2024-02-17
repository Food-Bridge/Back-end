from rest_framework import serializers
from ..models import Blog, Comment
from users.models import User

##### 사용자 정보 시리얼라이저
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', )

##### POST 요청(게시글 생성) 시리얼라이저
class PostCreateUpdateSerializer(serializers.ModelSerializer):
    author = UserInfoSerializer(read_only=True) ##### 현재 유저 정보 파악

    class Meta:
        model = Blog
        fields = ('author', 'title', 'content', 'created_at', 'updated_at')

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

##### GET 요청(전체 게시글 조회) 시리얼라이저
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

##### GET/PUT/DELETE 요청(상세 보기 조회, 수정, 삭제) 시리얼라이저
class PostDetailSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField(read_only=True)
    pk = serializers.SerializerMethodField(read_only=True)
    like_users = serializers.SerializerMethodField(read_only=True)
    comment_count = serializers.SerializerMethodField(read_only=True)  # SerializerMethodField로 변경
    author = UserInfoSerializer(read_only=True) ##### 현재 유저 정보 파악

    class Meta:
        model = Blog
        fields = ('pk', 'author', 'title', 'content', 'created_at', 'updated_at', 'like_users', 'comment_count', 'views', 'likes_count',)
    
    ##### 작성한 게시물의 번호 파라미터 -> pk
    def get_pk(self, obj):
        return obj.pk

    def get_likes_count(self, obj):
        return obj.like_users.count()
    
    def get_like_users(self, obj):
        like_users = obj.like_users.all()
        return UserInfoSerializer(like_users, many=True).data

    def get_comment_count(self, obj):
        return obj.comment_set.count()  # 해당 게시물의 댓글 수 반환

##### GET 요청(특정 게시물에 대한 모든 댓글 조회) 시리얼라이저
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

##### POST 요청(댓글 달기) 시리얼라이저
class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)

##### GET/PUT/DELETE 요청(댓글 상세 조회, 수정, 삭제) 시리얼라이저
class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content',)

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