from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy

from .models import User
from .forms import (
    UserRegisterForm,
    UserLoginForm,
    UpdatePasswordForm,
    UpdateProfileForm,
)


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


class UserLogoutView(LogoutView):
    """ユーザーログアウトビュー"""

    next_page = "/"
    success_message = "ログアウトしました｡"

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.info(self.request, self.success_message)
        return response


class UserView(LoginRequiredMixin, TemplateView):
    """ユーザービュー"""

    template_name = "user/user.html"

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UpdatePasswordView(LoginRequiredMixin, PasswordChangeView):
    """パスワード更新ビュー"""

    template_name = "user/update/update_password.html"
    form_class = UpdatePasswordForm
    success_url = reverse_lazy("user:login")
    success_message = "パスワードが更新されたました｡再ログインしてください｡"  # パスワード更新成功メッセージ

    def form_valid(self, form):
        messages.info(self.request, self.success_message)
        response = super().form_valid(form)
        logout(self.request)  # パスワードを更新後､自動ログアウトする
        return response


class UpdatePasswordDoneView(PasswordChangeDoneView):
    """パスワード変更完了ビュー"""

    template_name = "user/login.html"


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """ユーザープロフィール更新ビュー"""

    model = User
    template_name = "user/update/update_profile.html"
    form_class = UpdateProfileForm
    success_url = reverse_lazy("user:user")
    success_message = "プロフィールが変更されました｡"

    def get_object(self, queryset=None):
        """ログイン中のユーザーオブジェクトを取得"""
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            "プロフィールの更新に失敗しました。入力内容を確認してください。",
        )
        return super().form_invalid(form)


def page_not_found(request, exception):
    """404エラー処理"""
    return render(request, "error/404.html", status=404)
