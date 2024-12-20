from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model, authenticate
from django.core import validators
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
            raise forms.ValidationError("密码长度至少为8位！")
        if not any(char.isdigit() for char in new_password):
            raise forms.ValidationError("密码必须包含至少一个数字！")
        if not any(char.isalpha() for char in new_password):
            raise forms.ValidationError("密码必须包含至少一个字母！")
        return new_password


class UpdateProfileForm(forms.ModelForm):
    """ユーザープロフィール更新フォーム"""

    def save(self, *args, **kwargs):
        user = super(UpdateProfileForm, self).save(commit=False)
        user.save()
        return user

    class Meta:
        model = User
        fields = [
            "name",
        ]
