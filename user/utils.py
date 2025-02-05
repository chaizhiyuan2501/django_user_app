import uuid
import os

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
        """
        Django にこのオブジェクトをどのようにシリアライズするかを伝えます。
        """
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
