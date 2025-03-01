from django import forms
from django.utils import timezone

from .models import Todo


class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo
        fields = ("title", "expire_date", "finished_date", "description")

        labels = {
            "title": "タイトル",
            "finished_date": "有効期限",
            "description": "詳細",
        }
