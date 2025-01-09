from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve, reverse_lazy
from django.core.files.uploadedfile import SimpleUploadedFile

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
LOGOUT_USER_URL = reverse("user:logout")  # ログアウトページのURL


def create_user(**params):
    """新しいユーザーを作成する"""
    return get_user_model().objects.create_user(**params)


def get_update_password_url(user_id):
    """ユーザーパスワード更新のurl"""
    return reverse("user:update_password", kwargs={"pk": user_id})


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
        """メールアドレスを持つユーザーが存在する場合、フォームエラーが返されます。"""
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
            errors=[
                "この メールアドレス を持った ユーザー が既に存在します。",
            ],
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
            errors=[
                "パスワードの長さは8桁以上入力してください｡",
                "この値が少なくとも 8 文字以上であることを確認してください (7 文字になっています)。",
            ],
        )
        # 作成したユーザーのメールアドレスの数は0
        self.assertEqual(User.objects.filter(email=params["email"]).count(), 0)


def test_user_can_login(self):
    """ユーザーログインテスト"""
    user = create_user(
        email="test@example.com",
        password="testPass123",
        name="TestName",
    )
    response = self.client.post(
        LOGIN_USER_URL,
        {
            "username": "test@example.com",
            "password": "testPass123",
        },
    )
    self.assertEqual(response.status_code, 302)  # Redirect to dashboard
    self.assertIn("_auth_user_id", self.client.session)


class PrivateUserApiTests(TestCase):

    def setUp(self):
        self.email = "test@example.com"
        self.password = "testPass123"
        self.name = "TestName"
        self.user = create_user(
            email=self.email,
            password=self.password,
            name=self.name,
        )
        self.client = Client()
        # self.client.login(email="test@example.com", password="testPass123")
        self.client.force_login(self.user)

    def test_password_change(self):
        """パスワード変更テスト"""
        new_password = "NewPassword123"
        payload = {
            "old_password": self.password,
            "new_password1": new_password,
            "new_password2": new_password,
        }
        response = self.client.post(get_update_password_url(self.user.id), payload)

        # 确保视图返回正确状态码
        self.assertEqual(response.status_code, 302)

        # 验证密码是否已更新
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))  # 验证新密码

    def test_password_change_incorrect_old_password(self):
        new_password = "NewPassword123"
        payload = {
            "old_password": "wrongPass123",
            "new_password1": new_password,
            "new_password2": new_password,
        }
        response = self.client.post(get_update_password_url(self.user.id), payload)
        # 确保视图返回正确状态码
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "Your old password was entered incorrectly.")

        # 验证密码是否已更新
        self.user.refresh_from_db()
        self.assertTrue(
            self.user.check_password(self.password)
        )  # パスワードの変更ができなかった

    def test_password_change_password_mismatch(self):
        """新しいパスワードとパスワード確認が一致しているかテストする"""
        payload = {
            "old_password": self.user.password,
            "new_password1": "NewPass123",
            "new_password2": "MismatchPass123",
        }
        response = self.client.post(get_update_password_url(self.user.id), payload)
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "The two password fields didn't match") # エラー情報
        self.user.refresh_from_db()
        self.assertTrue(
            self.user.check_password(self.password)
        )  # パスワードの変更ができなかった

    def test_password_change_password_too_simple(self):
        """新しいパスワードが簡単すぎる場合のテスト"""
        payload = {
            "old_password": self.user.password,
            "new_password1": "123",
            "new_password2": "123",
        }
        response = self.client.post(get_update_password_url(self.user.id), payload)
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "This password is too short.") # エラー情報
        self.user.refresh_from_db()
        self.assertTrue(
            self.user.check_password(self.password)
        )  # パスワードの変更ができなかった

    def test_user_can_logout(self):
        """ユーザーログアウトテスト"""
        response = self.client.get(LOGOUT_USER_URL)
        self.assertEqual(response.status_code, 302)  # ログアウト後ダイレクトする
        self.assertNotIn("_auth_user_id", self.client.session)