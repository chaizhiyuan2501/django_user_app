from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from datetime import datetime

from .models import User
from .utils import check_password


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
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = "パスワード"

        self.fields["old_password"].label = "現在のパスワード"
        self.fields["new_password1"].label = "新しいパスワードを入力してください"
        self.fields["new_password2"].label = "新しいパスワードを再入力してください"

    def clean_new_password1(self):
        # カスタムのパスワード検証ロジックを追加
        new_password = self.cleaned_data.get("new_password1")

        # パスワードの長さが8文字未満の場合、バリデーションエラーを発生させる
        if len(new_password) < 8:
            raise forms.ValidationError(
                "パスワードの長さは少なくとも8文字以上である必要があります！"
            )

        # パスワードに少なくとも1つの数字が含まれていない場合、エラーを発生させる
        if not any(char.isdigit() for char in new_password):
            raise forms.ValidationError(
                "パスワードには少なくとも1つの数字を含める必要があります！"
            )

        # パスワードに少なくとも1つのアルファベットが含まれていない場合、エラーを発生させる
        if not any(char.isalpha() for char in new_password):
            raise forms.ValidationError(
                "パスワードには少なくとも1つの英字を含める必要があります！"
            )

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

    def save(self, commit=True):
        """ユーザーのプロフィール情報を保存する"""
        user = self.instance

        # フォームのクリーニング後のデータを取得し、値があるフィールドのみ更新する
        for field, value in self.cleaned_data.items():
            if value:  # 空でない値のみ処理する
                setattr(user, field, value)

        user.update_date = datetime.now()
        if commit:
            user.save()

        return user

    def clean_avatar(self):
        """アバター画像のサイズチェック"""
        avatar = self.cleaned_data.get("avatar")

        if not avatar:
            return avatar

        try:
            width, height = get_image_dimensions(avatar)

            max_size = 1000
            if width > max_size or height > max_size:
                raise ValidationError(
                    "アバター画像は1000x1000ピクセル以下である必要があります。"
                )

        except Exception as e:
            raise ValidationError(e)

        return avatar

    def clean_phone_number(self):
        """
        電話番号のバリデーションを行う
        """
        phone_number = self.cleaned_data.get("phone_number")

        # 電話番号が重複かどうかをチェック
        if phone_number and User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("指定された電話番号は既に登録されています。")

        return phone_number

    class Meta:
        model = User
        fields = [
            "name",
            "avatar",
            "phone_number",
        ]
