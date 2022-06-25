from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
  path('', views.index, name='index'),
  path('about/', views.about, name='about'),
  path('list/', views.post_list, name='post_list'),
  path('detail/<int:post_id>', views.post_detail, name='post_detail'),
  path('create/', views.post_create, name='post_create'),
  path('update/<int:post_id>', views.post_update, name='post_update'),
  path('delete/<int:post_id>', views.post_delete, name='post_delete'),
  path('comment/create/<int:post_id>', views.comment_create, name='comment_create'),
  path('comment/update/<int:comment_id>', views.comment_update, name='comment_update'),
  path('comment/delete/<int:comment_id>', views.comment_delete, name='comment_delete'),
]