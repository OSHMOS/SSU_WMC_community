from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('detail/<int:post_id>', views.post_detail, name='post_detail')
]