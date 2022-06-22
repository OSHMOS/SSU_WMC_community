from django import forms
from .models import Post

class Postform(forms.ModelForm):
    class Meta:
      model = Post
      exclude = ('author',)