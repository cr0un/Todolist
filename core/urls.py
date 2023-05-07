from django.urls import path
from . import views
from .views import LoginView, UpdatePasswordView


urlpatterns = [
    path('signup', views.UserRegistrationView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login_user'),
    path('profile', views.UserProfileView.as_view(), name='profile'),
    path('update_password', UpdatePasswordView.as_view(), name='update_password'),

    path('logged-in', views.logged_in, name='logged-in'),
    path('login-error', views.login_error, name='login-error'),
]