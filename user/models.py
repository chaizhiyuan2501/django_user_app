from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)

from user.utils import GetImagePath


class UserManager(BaseUserManager):
    """ユーザーマネジャーモデル"""

    def create_user(self, name, email, password=None, **extra_fields):
        user = self.model(
            name=name,
            email=self.normalize_email(email),  # 電子メールを正規化します
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password, **extra_fields):
        user = self.create_user(
            name=name,
            email=self.normalize_email(email),
            password=password,
            **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ユーザーモデル"""

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="ユーザー名",
    )
    email = models.EmailField(
        max_length=150,
        unique=True,
        verbose_name="メールアドレス",
    )
    avatar = models.ImageField(
        upload_to=GetImagePath("avatar/"),
        null=True,
        blank=True,
        verbose_name="アバター",
    )
    phone_number = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        verbose_name="携帯番号",
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    update_date = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    EMAIL_FIELD = "email"  # メールアドレスとして扱うフィールドの指定
    USERNAME_FIELD = "email"  # ユーザーを一意に識別するフィールドの指定
    REQUIRED_FIELDS = [
        "name"
    ]  # createsuperuser コマンド実行時に入力受付を行うフィールドの指定

    objects = UserManager()

    class Meta:
        verbose_name = "ユーザー"

    def __str__(self):
        return self.name
