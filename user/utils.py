import uuid
import os
import io
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from django.core import validators


class GetImagePath:
    """カスタマイズされた画像パスを取得します。
    :param prefix: 画像パスのプレフィックス
    :param instance: インスタンス (models.Model)
    :param filename: 元のファイル名
    :return: カスタマイズされたファイル名を含む画像パス
    """

    def __init__(self, prefix):
        self.prefix = prefix

    def __call__(self, instance, filename):
        name = str(uuid.uuid4()).replace("-", "")
        extension = os.path.splitext(filename)[-1]
        return self.prefix + name + extension

    def deconstruct(self):
        return (
            "user.utils.GetImagePath",  # クラスの完全パス
            [],  # 位置引数なし
            {"prefix": self.prefix},  # キーワード引数
        )


def check_password(password):
    # パスワードの長さをチェックする関数

    # パスワードが8文字以上でない場合、バリデーションエラーを発生させる
    if not (8 <= len(password)):
        raise validators.ValidationError("パスワードの長さは8桁以上入力してください｡")


def get_test_image(size=(400, 400), name="test_avatar.jpg", format="JPEG"):
    """指定サイズのテスト用画像を作成"""
    img = Image.new("RGB", size, (255, 0, 0))  # 赤色の画像
    img_io = io.BytesIO()
    img.save(img_io, format=format)
    img_io.seek(0)
    return SimpleUploadedFile(name, img_io.getvalue(), content_type="image/jpeg")
