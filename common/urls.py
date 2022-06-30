from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(
    #     template_name='account/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('signup/', views.signup, name='signup'),
    # path('password_reset/', views.UserPasswordResetView.as_view(), name="password_reset"),
    # path('password_reset_done/', views.UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    # path('password_reset_confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    # path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]