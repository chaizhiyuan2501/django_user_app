from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView, View
from django.views.generic import FormView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout,authenticate
from django.utils.decorators import method_decorator
from django.shortcuts import resolve_url
from django.urls import reverse_lazy

from .models import User
from .forms import UserRegisterForm, UserLoginForm, CustomUpdatePasswordForm


class HomeView(TemplateView):
    template_name = "home.html"


class UserRegisterView(CreateView):
    """ユーザー登録ビュー"""

    template_name = "user/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("user:home")
    success_message = "ユーザー登録成功しました｡"  # 登録成功メッセージ

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data.get("email")
        raw_pw = form.cleaned_data.get("password")
        user = authenticate(username=email, password=raw_pw)
        login(self.request, user)
        messages.success(self.request, self.success_message)  # 成功メッセージを追加
        return response


class UserLoginView(LoginView):
    "ユーザーログインビュー"

    template_name = "user/login.html"
    authentication_form = UserLoginForm  # カスタム認証フォームを指定する
    next_page = "/user"
    success_message = "ログインしました｡"  # ログイン成功メッセージ

    def form_valid(self, form):
        """フォームのバリデーションが成功したら"""
        # 記憶するオプションを処理
        remember = form.cleaned_data["rememberMe"]

        if remember:
            session_time = 24  # 有効期限の時間(24時間)を設定する
            self.request.session.set_expiry(
                3600 * session_time
            )  # ユーザのログイン情報の有効期限を設定する

        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class UpdatePasswordView(PasswordChangeView):
    """ユーザー更新ビュー"""

    template_name = "user/update.html"
    form_class = CustomUpdatePasswordForm
    success_url = reverse_lazy("user:login")
    success_message = "パスワードが更新されたました｡再ログインしてください｡"  # パスワード更新成功メッセージ

    def form_valid(self, form):
        messages.info(self.request, self.success_message)
        response = super().form_valid(form)
        logout(self.request)  # パスワードを更新後､自動ログアウトする
        return response


class UserLogoutView(LogoutView):
    """ユーザーログアウトビュー"""

    next_page = "/"
    success_message = "ログアウトしました｡"

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class UserView(LoginRequiredMixin, TemplateView):
    """ユーザービュー"""

    template_name = "user/user.html"

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def page_not_found(request, exception):
    """404エラー処理"""
    return render(request, "error/404.html", status=404)
