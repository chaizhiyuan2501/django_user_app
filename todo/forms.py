from django import forms
from django.utils import timezone

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
            pass

        def clean_expire_date(self):
            pass

        def clean(self):
            pass
