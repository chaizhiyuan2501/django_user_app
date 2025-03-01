from django.db import models
from django.conf import settings
from django.utils import timezone

from utils.db import BaseModel


class Todo(BaseModel):
    """Todoモデル"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name="タイトル")
    description = models.CharField(max_length=255,blank=True, null=True, verbose_name="詳細")
    registration_date = models.DateField(blank=True, null=True, verbose_name="登録日")
    expire_date = models.DateField(blank=True, null=True, verbose_name="有効期限")
    finished_date = models.DateField(blank=True, null=True, verbose_name="終了日")
    is_completed = models.BooleanField(default=False, verbose_name="達成フラグ")

    def __str__(self):
        return self.title

    @property
    def is_finished(self):
        """タスクが完了しているかどうかを判定（終了日がある場合はTrue）"""
        return self.finished_date is not None

    @property
    def is_expired(self):
        """タスクが期限切れかどうかを判定（現在時刻と比較）"""
        return self.expire_date and self.expire_date < timezone.now()

    def save(self, *args, **kwargs):
        """タスクを保存する際に更新日時を自動更新"""
        self.update_date_time = timezone.now()
        super.save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """タスクを削除する代わりに、is_deleted フラグをTrueにする"""
        self.is_deleted = True
        self.save()
