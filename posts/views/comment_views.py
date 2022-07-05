from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import messages
from posts.models import Post, Comment
from posts.forms import CommentForm

# Create your views here.

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
    if comment.author == request.user:
        comment.delete()
    return redirect('posts:post_detail', post_id=comment.post.id)


@login_required(login_url='account_login')
def comment_like(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.like.filter(id=request.user.id).exists():
        comment.like.remove(request.user)
    else:
        comment.like.add(request.user)
    return redirect('posts:post_detail', post_id=comment.post.id)