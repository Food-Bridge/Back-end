from django.db import models
from users.models import User
from django.shortcuts import reverse

# Create your models here.
##### image필드는 토요일에 회의 후 넣게 된다면 여기다가 추가할 것
##### 게시물 모델
class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ##### 좋아요 누른 사람들 : N : N 관계
    like_users = models.ManyToManyField(User, related_name='like_articles')
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)  ##### 조회 수 필드
    comment_count = models.IntegerField(default=0)  ##### 댓글 수 필드

    ##### 인기글 선정 기준 : 댓글 수 + 조회 수 + 게시글 좋아요 수
    def get_api_url(self):
        try:
            return reverse("posts_api:post_detail", kwargs={"pk":self.pk})
        except:
            None

##### 댓글 모델
##### 게시글 삭제 시 -> 댓글도 자동 삭제
class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment_likes = models.IntegerField(default=0)