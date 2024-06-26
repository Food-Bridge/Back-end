from django.db import models
from users.models import User
from django.shortcuts import reverse

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(User, related_name='like_articles')
    title = models.CharField(max_length=50, blank=False)
    content = models.CharField(max_length=500, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def standard_method(self):
        return self.like_users.count() + self.comment.count()    
    
    def get_api_url(self):
        try:
            return reverse("posts_api:post_detail", kwargs={"pk":self.pk})
        except:
            None

    def get_comment_count(self):
        return self.comment.count()
    
    def get_likes_count(self):
        return len(self.like_users)

class PostImage(models.Model):
    """이미지 모델"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="img")
    image = models.ImageField(upload_to="community/%Y/%m/%d", null=True, blank=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.IntegerField(default=0)

    def get_comment_count(self):
        return Comment.objects.filter(post=self.post).count()