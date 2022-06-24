from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post
from .forms import Postform

# Create your views here.
def index(request):
    return render(request, 'posts/index.html')


def post_list(request):
    post_list = Post.objects.order_by('-dt_created')
    paginator = Paginator(post_list, 10)
    curr_page_num = request.GET.get("page")
    if curr_page_num == None:
        curr_page_num = 1
    page = paginator.page(curr_page_num)
    ctx = {"post_list": page}
    return render(request, 'posts/post_list.html', ctx)


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
            return redirect('posts:post_list')
    else:
        form = Postform()
    ctx = {'form' : form}
    return render(request, 'posts/post_form.html', ctx)


@login_required(login_url='account_login')
def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == "POST":
        form = Postform(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:post_detail', post.id)
    else:
        if post.author == request.user:
            form = Postform(instance=post)
        else:
            ctx = {'post' : post}
            return render(request, 'posts/post_not_access.html', ctx)
    ctx = {'form' : form}
    return render(request, 'posts/post_update.html', ctx)


@login_required(login_url='account_login')
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author == request.user:
        post.delete()
    else:
        ctx = {'post' : post}
        return render(request, 'posts/post_not_access.html', ctx)
    return redirect('posts:post_list')