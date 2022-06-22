from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('detail/<int:post_id>', views.post_detail, name='post_detail'),
  path('create/', views.post_create, name='post_create'),
  path('update/<int:post_id>', views.post_update, name='post_update'),
]