from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve, reverse_lazy
from ..models import User
from user.views import (
    UserLoginView,
    UserLogoutView,
    UserRegisterForm,
    HomeView,
    UserView,
)

CREATE_USER_URL = reverse("user:register")  # ユーザ登録ページのURL
LOGIN_USER_URL = reverse("user:login")  # ログインページのURL


def create_user(**params):
    """新しいユーザーを作成する"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """ユーザー API の公開機能をテストします。"""

    def test_create_user_successful(self):
        """ユーザーを作成し､ホームページに遷移が成功したかテストする"""
        # ユーザー作成するための仮パラメータ
        params = {
            "name": "TestUser",
            "email": "test@example.com",
            "password": "testPass123",
        }
        # ユーザー登録ページをポストし､ユーザーを作成する
        response = self.client.post(CREATE_USER_URL, params)
        # ユーザーを作成し､ホームページに遷移できるかをテストする
        self.assertRedirects(response, reverse_lazy("user:home"))
        # 作成したユーザーの情報は情報のと一致しているかテストする
        user = get_user_model().objects.get(email=params["email"])
        self.assertTrue(user.name, params["name"])
        self.assertTrue(user.email, params["email"])
        self.assertTrue(user.check_password(params["password"]))

    def test_user_with_email_exists_error(self):
        """電子メールを持つユーザーが存在する場合、フォームエラーが返されます。"""
        params = {
            "name": "Test Name",
            "email": "test@example.com",
            "password": "testpass123",
        }
        # ユーザーを作成する
        create_user(**params)
        # 同じ情報のユーザーをもう一度作成する
        response = self.client.post(CREATE_USER_URL, params)
        # メールアドレスのフィールドに｢この メールアドレス を持った User が既に存在します。｣のエラーが発生するかテストする
        self.assertFormError(
            response=response,
            form="form",
            field="email",
            errors="この メールアドレス を持った User が既に存在します。",
        )
        # 作成したユーザーのメールアドレスの数は1つだけ
        self.assertEqual(User.objects.filter(email=params["email"]).count(), 1)

    def test_password_too_short_error(self):
        """パスワードが 8文字未満18以上の場合､フォームエラーが返されます。"""
        params = {
            "name": "Test name",
            "email": "test@example.com",
            "password": "p123456",
        }

        response = self.client.post(CREATE_USER_URL, params)
        # メールアドレスのフィールドに｢この メールアドレス を持った User が既に存在します。｣のエラーが発生するかテストする
        self.assertFormError(
            response=response,
            form="form",
            field="password",
            errors="パスワードの長さは8桁以上入力してください｡",
        )
        # 作成したユーザーのメールアドレスの数は0
        self.assertEqual(User.objects.filter(email=params["email"]).count(), 0)


class PrivateUserApiTests(TestCase):

    def setUp(self):
        pass