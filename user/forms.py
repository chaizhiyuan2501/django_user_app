from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.files.images import (
    get_image_dimensions,
)  # 開いているファイルまたはパスが指定されている場合、画像の (幅、高さ) を返します。
from datetime import datetime

from .models import User


def check_password(password):
    if not (8 <= len(password)):
        raise validators.ValidationError("パスワードの長さは8桁以上入力してください｡")


class UserRegisterForm(forms.ModelForm):
    """ユーザー登録フォーム"""

    name = forms.CharField(max_length=50, label="ユーザー名")
    email = forms.EmailField(max_length=150, label="メールアドレス")
    password = forms.CharField(
        min_length=8,
        label="パスワード",
        widget=forms.PasswordInput(),
        validators=[check_password],
    )

    def save(self, commit=False):
        user = super().save(commit=False)
        user.create_date = datetime.now()
        validate_password(self.cleaned_data["password"], user)
        user.set_password(self.cleaned_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ["name", "email", "password"]


class UserLoginForm(AuthenticationForm):
    """ユーザーログインフォーム"""

    username = forms.EmailField(label="メールアドレス")
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())
    rememberMe = forms.BooleanField(
        label="一定時間自動的にログイン", required=False, initial=False
    )


class UpdatePasswordForm(PasswordChangeForm):
    """パスワード更新フォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "class_name"
            field.widget.attrs["placeholder"] = "パスワード"

        self.fields["old_password"].label = "現在のパスワード"
        self.fields["new_password1"].label = "新しいパスワードを入力してください"
        self.fields["new_password2"].label = "新しいパスワードを再入力してください"

    def clean_new_password1(self):
        # 添加自定义密码验证逻辑
        new_password = self.cleaned_data.get("new_password1")
        if len(new_password) < 8:
            raise forms.ValidationError("密码长度至少为8位!")
        if not any(char.isdigit() for char in new_password):
            raise forms.ValidationError("密码必须包含至少一个数字！")
        if not any(char.isalpha() for char in new_password):
            raise forms.ValidationError("密码必须包含至少一个字母！")
        return new_password


class UpdateProfileForm(forms.ModelForm):
    """ユーザープロフィール更新フォーム"""

    name = forms.CharField(max_length=50, required=False, label="ユーザー名")
    phone_number = forms.CharField(max_length=50, required=False, label="携帯番号")
    avatar = forms.ImageField(
        required=False,
        label="アバター",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
    )

    def save(self, *args, **kwargs):
        user = self.instance
        # 遍历表单中的清理后数据，仅更新非空字段
        for field, value in self.cleaned_data.items():
            if value:  # 跳过空字段
                if field == "avatar":  # 对头像字段进行特殊处理
                    width, height = get_image_dimensions(value)
                    if width > 500 or height > 500:
                        raise ValidationError(
                            "アバター画像は500x500ピクセル以下である必要があります。"
                        )
                setattr(user, field, value)  # 动态更新字段
        user.update_date = datetime.now()
        user.save()
        return user

    def clean_phone_number(self):
        """
        電話番号のバリデーションを行う
        ー 入力された電話番号がすでに登録されたいるかを確認する
        ー 登録済みの場合､ValidationErrorをスローする

        Returns:
            phone_number (str):バリデーションを通過した電話番号

        Raises:
            ValidationError:電話番号がすでに登録されたいる場合
        """
        phone_number = self.cleaned_data.get("phone_number")
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("指定された電話番号は既に登録されています。")
        return phone_number

    class Meta:
        model = User
        fields = [
            "name",
            "avatar",
            "phone_number",
        ]
