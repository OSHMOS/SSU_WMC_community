from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import Postform

# Create your views here.
def index(request):
    posts = Post.objects.all()
    ctx = {'posts' : posts}
    return render(request, 'posts/index.html', ctx)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    ctx = {'post' : post}
    return render(request, 'posts/post_detail.html', ctx)


@login_required(login_url='account_login')
def post_create(request):
    if request.method == "POST":
        form = Postform(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = Postform()
    ctx = {'form' : form}
    return render(request, 'posts/post_form.html', ctx)