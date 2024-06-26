import datetime

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import F, Count
from django.db import transaction
from django.core.files.uploadedfile import UploadedFile

from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from .permissions import IsCommentOwner
from ..models import Post, Comment, PostImage
from community.api.serializers import (PostCreateUpdateSerializer, 
                                       PostListSerializer, 
                                       PostDetailSerializer, 
                                       CommentSerializer, 
                                       CommenterSerializer,
                                       CommentCreateUpdateSerializer,
                                       PostLikeSerializer)
from community.api.pagination import PostLimitOffsetPagination
from community.api.mixins import MutlipleFieldMixin

class ListPostAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [AllowAny]
    pagination_class = PostLimitOffsetPagination

class CreatePostAPIView(APIView):
    queryset = Post.objects.all()   
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
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        image_set = request.FILES.getlist('img')
        if image_set:
            instance.img.all().delete()
            for image_data in image_set:
                if isinstance(image_data, UploadedFile):
                    PostImage.objects.create(post=instance, image=image_data)

        instance.title = serializer.validated_data.get('title', instance.title)
        instance.content = serializer.validated_data.get('content', instance.content)
        instance.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListCommentAPIView(APIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CreateCommentAPIView(APIView):
    serializer_class = CommentCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        serializer = CommentCreateUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"errors" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class DetailCommentAPIView(MutlipleFieldMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsCommentOwner]
    queryset = Comment.objects.all()
    serializer_class = CommentCreateUpdateSerializer

class LikeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        serializer = PostLikeSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
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
        latest_posts = Post.objects.all().order_by('-created_at')[:10]
        serializer = PostListSerializer(latest_posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DailyPopularPostAPIView(APIView):
    serializer_class = PostListSerializer
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        today = timezone.localtime(timezone.now())
        start_of_today = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_today = today.replace(hour=23, minute=59, second=59, microsecond=0)

        popular_posts = Post.objects.filter(created_at__range=[start_of_today, end_of_today])
        popular_posts = popular_posts.annotate(comment_count=Count('comment'), like_users_count=Count('like_users'))
        popular_posts = popular_posts.annotate(total_weight=F('comment_count') + F('like_users_count')).order_by('-total_weight')[:10]
        serializer = PostListSerializer(popular_posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class WeekPopularPostAPIView(APIView):
    serializer_class = PostListSerializer
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        start_of_week = timezone.localtime(timezone.now()) - datetime.timedelta(days=timezone.localtime(timezone.now()).weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_week = start_of_week + datetime.timedelta(days=6, hours=23, minutes=59, seconds=59)

        if timezone.localtime(timezone.now()).weekday() == 0 and timezone.localtime(timezone.now()).hour == 0 and timezone.localtime(timezone.now()).minute == 0 and timezone.localtime(timezone.now()).second == 0:
            start_of_week = start_of_week - datetime.timedelta(days=7)
            end_of_week = end_of_week - datetime.timedelta(days=7)

        popular_posts = Post.objects.filter(created_at__range=[start_of_week, end_of_week])
        popular_posts = popular_posts.annotate(comment_count=Count('comment'),  like_users_count=Count('like_users'))
        popular_posts = popular_posts.annotate(total_weight=F('comment_count') + F('like_users_count')).order_by('-total_weight')[:10]
        serializer = PostListSerializer(popular_posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)