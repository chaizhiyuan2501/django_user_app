from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from user.models import User
from user.forms import UpdateProfileForm
from unittest.mock import patch
from django.contrib.auth import get_user_model
from user import forms

def create_user(**params):
    """新しいユーザーを作成する"""
    return get_user_model().objects.create_user(**params)

class UpdateProfileFormTest(TestCase):
    def setUp(self):
        # テスト用のユーザーを作成
        self.email = "test@example.com"
        self.password = "testPass123"
        self.name = "TestName"
        self.user = create_user(
            email=self.email,
            password=self.password,
            name=self.name,
            phone_number="123456789",
            avatar="default/default_avatar.jpg",  # 使用默认头像
        )

    def test_avatar_upload_success(self):
        """アバター画像が正常にアップロードされることをテスト"""
        # 画像ファイルをシミュレート
        avatar = SimpleUploadedFile(
            name="test_avatar.jpg",
            content=b"fake_image_data",
            content_type="image/jpeg"
        )

        # フォームデータを作成
        form_data = {
            "name": "New Name",
            "phone_number": "1234567890",
        }
        form_files = {
            "avatar": avatar
        }

        # フォームのインスタンスを作成
        form = UpdateProfileForm(data=form_data, files=form_files, instance=self.user)

        # フォームが有効であることを確認
        self.assertTrue(form.is_valid())

        # フォームを保存
        user = form.save()

        # アップロードされたアバターが保存されていることを確認
        self.assertTrue(user.avatar.url.endswith("test_avatar.jpg"))
        self.assertEqual(user.name, "New Name")
        self.assertEqual(user.phone_number, "1234567890")

    def test_avatar_upload_invalid_size(self):
        """アバター画像が500x500ピクセルを超える場合、エラーを発生させることをテスト"""
        # サイズの大きな画像ファイルをシミュレート（Fake Content）
        avatar = SimpleUploadedFile(
            name="large_avatar.jpg",
            content=b"fake_large_image_data",
            content_type="image/jpeg"
        )

        # モック get_image_dimensions を使用して画像のサイズをシミュレート
        with self.settings(DEBUG=True), self.assertRaises(forms.ValidationError):
            with patch("user.forms.get_image_dimensions") as mock_get_image_dimensions:
                mock_get_image_dimensions.return_value = (600, 600)  # 超過サイズを設定

                # フォームデータを作成
                form_data = {
                    "name": "New Name",
                    "phone_number": "1234567890",
                }
                form_files = {
                    "avatar": avatar
                }

                # フォームのインスタンスを作成
                form = UpdateProfileForm(data=form_data, files=form_files, instance=self.user)

                # フォームのバリデーション
                self.assertFalse(form.is_valid())

                # エラーメッセージを確認
                self.assertIn("アバター画像は500x500ピクセル以下である必要があります。", form.errors["avatar"])
