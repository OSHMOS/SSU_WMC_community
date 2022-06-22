from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.
def index(request):
    posts = Post.objects.all()
    ctx = {'posts' : posts}
    return render(request, 'posts/index.html', ctx)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    ctx = {'post' : post}
    return render(request, 'posts/post_detail.html', ctx)