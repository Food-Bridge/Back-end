import datetime

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import F, Count
from django.db import transaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from .permissions import IsOwnerOrReadOnly
from ..models import Blog, Comment
from community.api.serializers import (PostCreateUpdateSerializer, 
                                       PostListSerializer, 
                                       PostDetailSerializer, 
                                       CommentSerializer, 
                                       CommentCreateUpdateSerializer,
                                       PostLikeSerializer,
                                       PopularPostSerializer)
from community.api.pagination import PostLimitOffsetPagination
from community.api.mixins import MutlipleFieldMixin

class ListPostAPIView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [AllowAny]
    pagination_class = PostLimitOffsetPagination

class CreatePostAPIView(APIView):
    queryset = Blog.objects.all()   
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        mutable_data = request.data.copy()
        mutable_data['author'] = user_id
        serializer = PostCreateUpdateSerializer(data=mutable_data, context={'request': request})
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(author_id=user_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DetailPostAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        tomorrow = datetime.datetime.replace(timezone.datetime.now(), hour=23, minute=59, second=0)
        expires = datetime.datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")

        serializer = self.get_serializer(instance)
        response = Response(serializer.data, status=status.HTTP_200_OK)

        if request.user.is_authenticated:
            user_id = request.user.id
            user_cookie_key = f'user_{user_id}_hit'

            if request.COOKIES.get(user_cookie_key) is not None:
                cookies = request.COOKIES.get(user_cookie_key)
                cookies_list = cookies.split("|")
                if str(pk) not in cookies_list:
                    response.set_cookie(user_cookie_key, cookies + f'|{pk}', expires=expires)
                    with transaction.atomic():
                        instance.views += 1
                        instance.save()
            else:
                # 쿠키가 없는 경우, 새로 생성해서 해당 게시물 번호를 저장
                response.set_cookie(user_cookie_key, f'{pk}', expires=expires)
                instance.views += 1
                instance.save()
        return response

class ListCommentAPIView(APIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get(self, request, pk):
        post = Blog.objects.get(pk=pk)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CreateCommentAPIView(APIView):
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
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Comment.objects.all()
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
        
class LatestPostsAPIView(APIView):
    serializer_class = PostListSerializer
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        latest_posts = Blog.objects.all().order_by('-created_at')[:10]
        serializer = PostListSerializer(latest_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DailyPopularPostAPIView(APIView):
    serializer_class = PopularPostSerializer
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        today = timezone.localtime(timezone.now())
        start_of_today = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_today = today.replace(hour=23, minute=59, second=59, microsecond=0)

        popular_posts = Blog.objects.filter(created_at__range=[start_of_today, end_of_today])
        popular_posts = popular_posts.annotate(comment_count=Count('comment'), like_users_count=Count('like_users'))
        popular_posts = popular_posts.annotate(total_weight=F('views') + F('comment_count') + F('like_users_count')).order_by('-total_weight')[:10]
        serializer = PopularPostSerializer(popular_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class WeekPopularPostAPIView(APIView):
    serializer_class = PopularPostSerializer
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        start_of_week = timezone.localtime(timezone.now()) - datetime.timedelta(days=timezone.localtime(timezone.now()).weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_week = start_of_week + datetime.timedelta(days=6, hours=23, minutes=59, seconds=59)

        if timezone.localtime(timezone.now()).weekday() == 0 and timezone.localtime(timezone.now()).hour == 0 and timezone.localtime(timezone.now()).minute == 0 and timezone.localtime(timezone.now()).second == 0:
            start_of_week = start_of_week - datetime.timedelta(days=7)
            end_of_week = end_of_week - datetime.timedelta(days=7)

        popular_posts = Blog.objects.filter(created_at__range=[start_of_week, end_of_week])
        popular_posts = popular_posts.annotate(comment_count=Count('comment'),  like_users_count=Count('like_users'))
        popular_posts = popular_posts.annotate(total_weight=F('views') + F('comment_count') + F('like_users_count')).order_by('-total_weight')[:10]
        serializer = PopularPostSerializer(popular_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)