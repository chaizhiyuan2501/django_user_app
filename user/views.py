from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView, View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.utils.decorators import method_decorator
from django.shortcuts import resolve_url
from django.urls import reverse_lazy

from .models import User
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm


def BaseView(request):
    if request.user.is_authenticated:
        user_data = User.objects.all().values()
    template = "base.html"
    context = {
        "user_data": user_data or "ゲスト",
    }
    return render(request, template, context)


class HomeView(TemplateView):
    template_name = "home.html"


class UserRegisterView(CreateView):
    """ユーザー登録ビュー"""

    template_name = "user/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("user:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data.get("email")
        raw_pw = form.cleaned_data.get("password")
        user = authenticate(username=email, password=raw_pw)
        login(self.request, user)
        return response


class UserLoginView(LoginView):
    "ユーザーログインビュー"

    template_name = "user/login.html"
    authentication_form = UserLoginForm  # カスタム認証フォームを指定する

    def form_valid(self, form):
        """フォームのバリデーションが成功したら､"""
        remember = form.cleaned_data["rememberMe"]
        if remember:
            session_hour = 24  # 有効期限の時間()を設定する
            self.request.session.set_expiry(
                3600 * session_hour
            )  # ユーザのログイン情報の有効期限を設定する
        return super().form_valid(form)

    def get_success_url(self):
        return resolve_url("user:user")

    def get_object(self):
        return self.request.user


@method_decorator(login_required, name="dispatch")
class UserUpdateView(UpdateView):
    """ユーザー更新ビュー"""

    model = User
    template_name = "user/update.html"
    form_class  = UserUpdateForm

    def get_success_url(self):
        return resolve_url("user:home")


class UserLogoutView(LogoutView):
    """ユーザーログアウトビュー"""

    next_page = "/"


class UserView(LoginRequiredMixin, TemplateView):
    """ユーザービュー"""

    template_name = "user/user.html"

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def page_not_found(request, exception):
    """404エラー処理"""
    return render(request, "error/404.html", status=404)
