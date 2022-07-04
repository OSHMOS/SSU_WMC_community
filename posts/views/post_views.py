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
    pk_url_kwarg = 'post_id'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('posts:post_detail', kwargs={'post_id' : self.object.id})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_update.html"
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.dt_updated = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('posts:post_detail', kwargs={'post_id' : self.object.id})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'

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