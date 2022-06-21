from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass


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