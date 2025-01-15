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
        default=None,
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
        constraints = [
            models.UniqueConstraint(
                fields=["phone_number"],
                name="unique_phone_number",
                condition=(
                    ~Q(phone_number=None)  # 仅在 phone_number 不为空时应用唯一性约束)
                    & ~Q(phone_number="")
                ),
            )
        ]

    def __str__(self):
        return self.name


@receiver(pre_save, sender=User)
def auto_delete_old_avatar(sender, instance, **kwargs):
    """
    自动删除用户的旧头像。
    """
    if instance.pk:  # 确保实例已存在
        try:
            old_avatar = User.objects.get(pk=instance.pk).avatar
        except User.DoesNotExist:
            return  # 用户不存在时不处理

        new_avatar = instance.avatar
        if (
            old_avatar
            and old_avatar != new_avatar
            and old_avatar.name != "default/default_avatar.jpg"
        ):
            old_avatar_path = old_avatar.path
            if os.path.isfile(old_avatar_path):
                try:
                    os.remove(old_avatar_path)
                    print(f"旧头像已删除: {old_avatar_path}")
                except Exception as e:
                    print(f"删除旧头像失败: {e}")
