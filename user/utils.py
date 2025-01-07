import uuid
import os


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
