from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView

from .permissions import IsOwnerOrReadOnly
from ..models import Blog, Comment
from community.api.serializers import (PostCreateUpdateSerializer, 
                                       PostListSerializer, 
                                       PostDetailSerializer, 
                                       CommentSerializer, 
                                       CommentCreateUpdateSerializer,
                                       PostLikeSerializer)
from community.api.pagination import PostLimitOffsetPagination
from community.api.mixins import MutlipleFieldMixin

##### 주간 인기글/일간 인기글 구현을 위한 정기적인 함수 실행 라이브러리
from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler()

class ListPostAPIView(generics.ListAPIView):
    """
    get:
        Returns a list of all existing posts
    """
    queryset = Blog.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [AllowAny]
    pagination_class = PostLimitOffsetPagination

class CreatePostAPIView(APIView):
    queryset = Blog.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    """
    post:
        Creates a new post instance. Returns created post data

        parameters: [title, content]
    """
    ##### Blog 모델에 아래와 같은 코드로 외래키를 지정
    ##### author = models.ForeignKey(User, on_delete=models.CASCADE)
    ##### 이 때, author에는 작성한 사용자의 아이디가 들어간다.
    ##### 다른 것을 알 필요없이 누가 썼는지에 대한 정보를 직렬화해서 이 값만을 넘겨주면 author 필드를 입력하지 않아도 됨(원래 그래야 함)
    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        request.data['author'] = user_id
        serializer = PostCreateUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author_id=user_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DetailPostAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
        Returns the details of a post instance. Searches post using pk field.

    put:
        Updates an existing post. Returns updated post data

        parameters: [slug, title, content]

    delete:
        Delete an existing post

        parameters = [pk]
    """
    queryset = Blog.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        return super().retrieve(request, *args, **kwargs)


class ListCommentAPIView(APIView):
    """
    get:
        Returns the list of comments on a particular post
    """
    permission_classes = [AllowAny]

    def get(self, request, pk):
        post = Blog.objects.get(pk=pk)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CreateCommentAPIView(APIView):
    """
    post:
        Create a comment instnace. Returns created comment data

        parameters: [pk, content]
    """
    serializer_class = CommentCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Blog, pk=pk)
        serializer = CommentCreateUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"errors" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class DetailCommentAPIView(MutlipleFieldMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    get:
        Returns the details of a comment instance. Searches comment using comment id and post pk in the url.

    put:
        Updates an existing comment. Returns updated comment data

        parameters: [post, author, content]

    delete:
        Delete an existing comment

        parameters: [post, author, content]
    """
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Comment.objects.all()
    lookup_field = ["post", "id"]
    serializer_class = CommentCreateUpdateSerializer

class LikeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        post = get_object_or_404(Blog, id=pk)
        serializer = PostLikeSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, pk):
        post = get_object_or_404(Blog, id=pk)
        if request.user in post.like_users.all():
            post.like_users.remove(request.user)
            post.save()
            return Response("unlike", status=status.HTTP_200_OK)
        else:
            post.like_users.add(request.user)
            post.save()
            return Response("like", status=status.HTTP_200_OK)