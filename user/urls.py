from django.urls import path
from .views import (
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    UpdatePasswordView,
    UpdateProfileView,
    HomeView,
    UserView,
)

app_name = "user"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("update_password/<int:pk>", UpdatePasswordView.as_view(), name="update_password"),
    path("update_profile/<int:pk>", UpdateProfileView.as_view(), name="update_profile"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("user/", UserView.as_view(), name="user"),
]
