import os
from django.test import TestCase
from django.contrib.auth import get_user_model

from unittest.mock import patch

from user.utils import GetImagePath


def create_user(name="testName", email="user@example.com", password="testpass123"):
    """Create and return a new user."""
    return get_user_model().objects.create_user(name, email, password)


class Model_Tests(TestCase):
    """モデルをテストする"""

    def test_create_user_with_email_successful(self):
        """メールを使用してユーザーを作成して成功したかのテスト"""
        name = "testName"
        email = "test@example.com"
        password = "TestPass123"
        user = get_user_model().objects.create_user(
            name=name, email=email, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """新規ユーザー向けにテストメールが標準化されたかのテスト。"""
        sample_emails_and_username = [
            ["test1@EXAMPLE.com", "test1@example.com", "testUser1"],
            ["Test2@Example.com", "Test2@example.com", "testUser2"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com", "testUser3"],
            ["test4@example.COM", "test4@example.com", "testUser4"],
        ]
        for email, expected, name in sample_emails_and_username:
            user = get_user_model().objects.create_user(
                name=name, email=email, password="sample123"
            )
            self.assertEqual(user.email, expected)

    @patch("uuid.uuid4")
    def test_generate_custom_image_path(self, mock_uuid):
        """GetImagePath クラスが正しいカスタム画像パスを生成することをテストする"""

        # モック UUID を設定
        mock_uuid.return_value = "test-uuid"

        # テスト対象のインスタンスを生成
        prefix = "media/avatar/"
        instance = None  # モデルインスタンスはテストでは必要ない
        filename = "example.jpg"

        # GetImagePath の呼び出し
        image_path_generator = GetImagePath(prefix)
        generated_path = image_path_generator(instance, filename)

        # 期待するパス
        expected_path = f"{prefix}testuuid.jpg"

        # アサーション
        self.assertEqual(generated_path, expected_path)

    def test_image_path(self):
        """GetImagePath クラスの動作をテスト"""
        get_image_path = GetImagePath("avatar/")
        file_path = get_image_path(None, "example.jpg")
        print(f"Generated file path: {file_path}")  # デバッグ用

        # 期待するパスを生成
        self.assertTrue(file_path.startswith("avatar/"))
        self.assertTrue(file_path.endswith(".jpg"))

        # 実際のファイルパス
        full_path = os.path.join("media", file_path)  # MEDIA_ROOT を考慮したフルパス

        # ファイルを仮に作成（通常テスト時に自動作成される）
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write("dummy data")

        # 確認: ファイルが存在する
        self.assertTrue(os.path.exists(full_path))

        # テスト後にファイルを削除
        if os.path.exists(full_path):
            os.remove(full_path)

        # ディレクトリも空の場合削除
        if os.path.exists(os.path.dirname(full_path)) and not os.listdir(os.path.dirname(full_path)):
            os.rmdir(os.path.dirname(full_path))
