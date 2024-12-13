from django.urls import path
from .views import (
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    UserUpdateView,
    HomeView,
    UserView,
)

app_name = "user"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("update/<int:pk>", UserUpdateView.as_view(), name="update"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("user/", UserView.as_view(), name="user"),
]
