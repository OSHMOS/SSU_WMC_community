from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.core.paginator import Paginator
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
from posts.models import Post
from posts.forms import PostForm

# def post_list(request):
#     post_list = Post.objects.order_by('-dt_created')
#     paginator = Paginator(post_list, 10)
#     curr_page_num = request.GET.get("page")
#     if curr_page_num == None:
#         curr_page_num = 1
#     page = paginator.page(curr_page_num)
#     ctx = {"post_list": page}
#     return render(request, 'posts/post_list.html', ctx)


class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    ordering = '-dt_created'
    paginate_by = 10
    page_kwarg = 'page'


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    ctx = {'post' : post}
    return render(request, 'posts/post_detail.html', ctx)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('posts:post_list')


@login_required(login_url='account_login')
def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        messages.error(request, '해당 게시글 수정 권한이 없습니다.')
        return redirect('posts:post_detail', post_id) 
    
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.dt_updated = timezone.now()
            post.author = request.user
            post.save()
            return redirect('posts:post_detail', post.id)
    else:
        form = PostForm(instance=post)
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
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if post.like.filter(id=request.user.id).exists():
        post.like.remove(request.user)
    else:
        post.like.add(request.user)
    return redirect('posts:post_detail', post_id)