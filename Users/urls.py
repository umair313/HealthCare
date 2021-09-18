from os import name
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import Home, register, profile_view

urlpatterns = [
    path("",Home,name="Home"),
    path("register/",register, name="register"),
    path("login/",auth_views.LoginView.as_view(template_name="users/login.html"),name="login"),
    path("logout/",auth_views.LogoutView.as_view(),name="logout"),
    path("profile/",profile_view,name="profile")

]