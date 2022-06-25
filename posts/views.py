from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import messages
from .models import Post, Comment
from .forms import Postform, CommentForm

# Create your views here.
def index(request):
    return render(request, 'posts/index.html')


def about(request):
    return render(request, 'about.html')


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

    if post.author != request.user:
        messages.error(request, '해당 게시글 수정 권한이 없습니다.')
        return redirect('posts:post_detail', post_id) 
    
    if request.method == "POST":
        form = Postform(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.dt_updated = timezone.now()
            post.author = request.user
            post.save()
            return redirect('posts:post_detail', post.id)
    else:
        form = Postform(instance=post)
    ctx = {'form' : form}
    return render(request, 'posts/post_update.html', ctx)


@login_required(login_url='account_login')
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        messages.error(request, '해당 게시글 삭제 권한이 없습니다.')
        return redirect('posts:post_detail', post_id)
    else:
        post.delete()
    return redirect('posts:post_list')


@login_required(login_url='account_login')
def comment_create(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('posts:post_detail', post_id)
    
    messages.error(request, '내용이 없는 댓글은 등록할 수 없습니다.')
    return redirect('posts:post_detail', post_id)
    

@login_required(login_url='account_login')
def comment_update(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        messages.error(request, '해당 댓글 수정 권한이 없습니다.')
        return redirect('posts:post_detail', post_id=comment.post.id)
    
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.dt_updated = timezone.now()
            comment.save()
            return redirect('posts:post_detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)
    ctx = {'form' : form, 'comment' : comment}
    return render(request, 'posts/comment_update.html', ctx)


@login_required(login_url='account_login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        messages.error(request, '해당 댓글 삭제 권한이 없습니다.')
        return redirect('posts:post_detail', post_id=comment.post.id)
    else:
        comment.delete()
    return redirect('posts:post_detail', post_id=comment.post.id)
