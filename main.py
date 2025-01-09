import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
from django import setup

setup()

from user.models import User

# 创建超级用户
if not User.objects.filter(email="admin@mail.com").exists():  # 检查是否已存在
    User.objects.create_superuser(
        name="admin",  # 超级用户名
        email="admin@mail.com",  # 超级用户邮箱
        password="adminPass123",  # 超级用户密码
    )
    print("SuperUserは作成した")
else:
    print("SuperUserは既に存在する。")

# 创建第一个普通用户
if not User.objects.filter(email="test1@mail.com").exists():  # 检查是否已存在
    User.objects.create_user(
        name="user1",
        email="test1@mail.com",
        password="testPass123",
    )
    print("'user1'は作成した")
else:
    print("'user1' は既に存在する。")

# 创建第二个普通用户
if not User.objects.filter(email="test2@mail.com").exists():  # 检查是否已存在
    User.objects.create_user(
        name="user2",
        email="test2@mail.com",
        password="testPass456",
    )
    print("'user2'は作成した")
else:
    print("'user2' は既に存在する。")
