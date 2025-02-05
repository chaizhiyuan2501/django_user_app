import os

# Djangoの設定モジュールを指定
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

from django import setup

# Djangoをセットアップ
setup()

from user.models import User

# スーパー ユーザーを作成
if not User.objects.filter(email="admin@mail.com").exists():  # 既に存在するか確認
    User.objects.create_superuser(
        name="admin",  # スーパー ユーザー名
        email="admin@mail.com",  # スーパー ユーザーのメールアドレス
        password="adminPass123",  # スーパー ユーザーのパスワード
    )
    print("SuperUserは作成した")
else:
    print("SuperUserは既に存在する。")

# 最初の一般ユーザーを作成
if not User.objects.filter(email="test1@mail.com").exists():  # 既に存在するか確認
    User.objects.create_user(
        name="user1",
        email="test1@mail.com",
        password="testPass123",
    )
    print("'user1'は作成した")
else:
    print("'user1' は既に存在する。")

# 2番目の一般ユーザーを作成
if not User.objects.filter(email="test2@mail.com").exists():  # 既に存在するか確認
    User.objects.create_user(
        name="user2",
        email="test2@mail.com",
        password="testPass456",
    )
    print("'user2'は作成した")
else:
    print("'user2' は既に存在する。")
