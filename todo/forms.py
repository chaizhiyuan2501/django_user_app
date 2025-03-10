from django import forms
from django.utils import timezone
from datetime import date

from .models import Todo


class TodoForm(forms.ModelForm):

    is_completed = forms.BooleanField(required=False, label="Done")

    class Meta:
        model = Todo
        fields = ("title", "expire_date", "finished_date", "description")
        # フィールドのラベル
        labels = {
            "title": "タイトル",
            "expire_date": "期限日",
            "description": "詳細",
        }
        # エラーメーセージ
        error_messages = {
            "title": {"required": "タスク名が入力されていません｡"},
            "expire_date": {"required": "期限日が入力されていません｡"},
        }
        # ウィジェット
        widgets = {"expire_date": forms.DateInput(attrs={"type": "date"})}

        def clean_title(self):
            """タイトルのバリデーション"""
            title = self.cleaned_data.get("title")
            if not title:
                raise forms.ValidationError("タイトルが必要です｡")
            if len(title) > 50:
                raise forms.ValidationError("タイトルは50文字以内で入力してください。")
            return title

        def clean_expire_date(self):
            expire_date = self.cleaned_data.get("expire_date")
            if expire_date and expire_date < date.today():
                raise forms.ValidationError(
                    "期限日は今日以降の日付を設定してください。"
                )
            return expire_date

        def clean_description(self):
            """詳細のバリデーション"""
            description = self.cleaned_data.get("description")
            if description and len(description) > 300:
                raise forms.ValidationError("詳細は300文字以内で入力してください。")
            return description

        def clean(self):
            pass
