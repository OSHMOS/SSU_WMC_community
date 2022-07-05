from django.db import models
from common.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(null=True, blank=True)
    like = models.ManyToManyField(User, blank=True, related_name='post_like')
    bookmark = models.ManyToManyField(User, blank=True, related_name='post_bookmark')

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(null=True, blank=True)
    like = models.ManyToManyField(User, blank=True, related_name='comment_like')

    def __str__(self):
        return self.content