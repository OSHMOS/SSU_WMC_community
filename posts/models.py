from django.db import models
from common.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='author'
    )
    dt_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='comment_author')
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.content