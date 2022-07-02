from django.urls import path
from .views import base_views, post_views, comment_views

app_name = "posts"

urlpatterns = [
  # base_views.py
  path('', base_views.index, name='index'),
  path('about/', base_views.about, name='about'),

  # post_views.py
  path('list/', post_views.PostListView.as_view(), name='post_list'),
  path('detail/<int:post_id>', post_views.PostDetailView.as_view(), name='post_detail'),
  path('create/', post_views.PostCreateView.as_view(), name='post_create'),
  path('update/<int:pk>', post_views.PostUpdateView.as_view(), name='post_update'),
  path('delete/<int:pk>', post_views.PostDeleteView.as_view(), name='post_delete'),
  path('like/<int:post_id>', post_views.post_like, name='post_like'),

  # comment_views.py
  path('comment/create/<int:post_id>', comment_views.comment_create, name='comment_create'),
  path('comment/update/<int:comment_id>', comment_views.comment_update, name='comment_update'),
  path('comment/delete/<int:comment_id>', comment_views.comment_delete, name='comment_delete'),
]