import os
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from user.forms import UpdateProfileForm
from django.contrib.auth import get_user_model
from django.conf import settings

from user.utils import get_test_image


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
        # テスト用にアップロードしたファイル名を管理する
        self.uploaded_files = []

    def test_profile_upload_success(self):
        """ユーザー情報が正常にアップロードされることをテスト"""
        # 画像ファイルをシミュレート
        avatar = get_test_image(size=(400, 400), name="test_avatar.jpg")

        # フォームデータを作成
        form_data = {
            "name": "New Name",
            "phone_number": "1234567890",
        }
        form_files = {"avatar": avatar}

        # フォームのインスタンスを作成
        form = UpdateProfileForm(data=form_data, files=form_files, instance=self.user)

        # フォームが有効であることを確認
        self.assertTrue(form.is_valid())

        # フォームを保存
        user = form.save()

        # テストで生成されたファイルの名前を記録
        self.uploaded_files.append(user.avatar.name)

        # アップロードされたアバターが適切なディレクトリに保存されていることを確認
        self.assertTrue(user.avatar.name.startswith("avatar/"))

        self.assertEqual(user.name, "New Name")
        self.assertEqual(user.phone_number, "1234567890")

    def test_avatar_upload_invalid_size(self):
        """1000*1000を超えるアバター画像をアップロードした場合のテスト"""
        image = get_test_image(size=(1100, 1100))  # サイズが大きすぎる画像

        form_data = {"avatar": image}
        form = UpdateProfileForm(data={}, files=form_data)

        self.assertFalse(form.is_valid())  # フォームが無効であることを確認
        self.assertIn("avatar", form.errors)

        # エラーメッセージの確認
        self.assertIn(
            "アバター画像は1000x1000ピクセル以下である必要があります。",
            form.errors["avatar"],
        )

    def tearDown(self):
        """テスト終了後にテストで作成した画像のみ削除"""
        for file_name in self.uploaded_files:
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
