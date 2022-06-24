from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
  path('', views.index, name='index'),
  path('list/', views.post_list, name='post_list'),
  path('detail/<int:post_id>', views.post_detail, name='post_detail'),
  path('create/', views.post_create, name='post_create'),
  path('update/<int:post_id>', views.post_update, name='post_update'),
  path('delete/<int:post_id>', views.post_delete, name='post_delete'),
]