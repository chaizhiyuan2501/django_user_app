from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm
from django.core import validators
from datetime import datetime
from .models import User


def check_password(password):
    if not (8 <= len(password)):
        raise validators.ValidationError("パスワードの長さは8桁以上入力してください｡")


class UserRegisterForm(forms.ModelForm):
    """ユーザー登録フォーム"""

    name = forms.CharField(label="名前")
    email = forms.EmailField(label="メールアドレス")
    password = forms.CharField(
        label="パスワード", widget=forms.PasswordInput(), validators=[check_password]
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

    email = forms.EmailField(label="メールアドレス")
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())
    rememberMe = forms.BooleanField(label="一定時間自動的にログイン", required=False)


class UserUpdateForm(forms.ModelForm):
    """ユーザー更新フォーム"""

    class Meta:
        model = User
        fields = ["name",]

    def save(self, *args, **kwargs):
        obj = super(UserUpdateForm, self).save(commit=False)
        # obj.update_at = datetime.now()
        obj.save()
        return obj
