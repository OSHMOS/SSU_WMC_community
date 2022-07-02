from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
from posts.models import Post
from posts.forms import PostForm


class PostListView(ListView):
    model = Post
    ordering = '-dt_created'
    paginate_by = 10



class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('posts:post_detail', kwargs={'pk' : self.object.id})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.error(request, '해당 게시글 수정 권한이 없습니다.')
            return redirect('posts:post_detail', object.id)
        else:
            return super(PostUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.dt_updated = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('posts:post_detail', kwargs={'pk' : self.object.id})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.error(request, '해당 게시글 삭제 권한이 없습니다.')
            return redirect('posts:post_detail', object.id)
        else:
            return super(PostDeleteView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('posts:post_list')


@login_required(login_url='account_login')
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if post.like.filter(id=request.user.id).exists():
        post.like.remove(request.user)
    else:
        post.like.add(request.user)
    return redirect('posts:post_detail', post_id)