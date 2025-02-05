import os
from django.db import models
from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import pre_save
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
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password, **extra_fields):
        user = self.create_user(
            name=name,
            email=self.normalize_email(email),
            password=password,
            **extra_fields,
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
        default="default/default_avatar.jpg",
        verbose_name="アバター",
    )
    phone_number = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        default="",
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
        # 携帯番号の一意性制約（NULLや空白を除く）
        constraints = [
            models.UniqueConstraint(
                fields=["phone_number"],
                name="unique_phone_number",
                condition=(
                    ~Q(phone_number=None)  # phone_numberがNULLでない場合のみ適用
                    & ~Q(phone_number="")  # 空文字列でない場合のみ適用
                ),
            )
        ]

    def __str__(self):
        return self.name


@receiver(pre_save, sender=User)
def auto_delete_old_avatar(sender, instance, **kwargs):
    """
    ユーザーの古いアバター画像を自動的に削除する。
    """
    if instance.pk:  # インスタンスが既に存在していることを確認
        try:
            old_avatar = User.objects.get(pk=instance.pk).avatar  # 現在のアバターを取得
        except User.DoesNotExist:
            return  # ユーザーが存在しない場合は処理を行わない

        new_avatar = instance.avatar  # 新しく設定されるアバター

        # 古いアバターが存在し、新しいアバターと異なり、デフォルト画像でない場合
        if (
            old_avatar
            and old_avatar != new_avatar
            and old_avatar.name != "default/default_avatar.jpg"
        ):
            old_avatar_path = old_avatar.path  # 古いアバターのファイルパスを取得
            if os.path.isfile(old_avatar_path):  # ファイルが存在するか確認
                try:
                    os.remove(old_avatar_path)  # 古いアバターを削除
                    print(f"古いアバターを削除しました: {old_avatar_path}")
                except Exception as e:
                    print(f"古いアバターの削除に失敗しました: {e}")
