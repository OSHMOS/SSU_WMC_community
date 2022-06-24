from django import forms
from .models import Post, Comment

class Postform(forms.ModelForm):
    class Meta:
      model = Post
      exclude = ('author', 'dt_updated',)


class CommentForm(forms.ModelForm):
    class Meta:
      model = Comment
      fields = ['content']