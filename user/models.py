from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """ """

    def create_user(self, name, email, password=None):
        user = self.model(
            name=name,
            email=self.normalize_email(email),  # 電子メールを正規化します
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password):
        user = self.create_user(name, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ユーザーモデル"""

    name = models.CharField(max_length=50, verbose_name="ユーザー名")
    email = models.EmailField(
        max_length=150, unique=True, verbose_name="メールアドレス"
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    EMAIL_FIELD = "email"   # メールアドレスとして扱うフィールドの指定
    USERNAME_FIELD = "email"  # ユーザーを一意に識別するフィールドの指定
    REQUIRED_FIELDS = ["name"] # createsuperuser コマンド実行時に入力受付を行うフィールドの指定

    objects = UserManager()
