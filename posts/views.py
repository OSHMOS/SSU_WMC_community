from django.shortcuts import render
from .models import Post

# Create your views here.
def index(request):
    posts = Post.objects.all()
    ctx = {'posts' : posts}
    return render(request, 'posts/index.html')