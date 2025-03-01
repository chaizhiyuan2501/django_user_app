from user.models import User
from django.db import models


def get_user_model_data(request):
    if request.user.is_authenticated:
        # 用户已登录，获取模型数据
        data = User.objects.all().values()  # 根据需求修改查询逻辑
        return data
    else:
        # 用户未登录，返回空数据
        return "ゲスト"


class BaseModel(models.Model):
    """ベースモデル"""

    create_date_time = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    update_date_time = models.DateTimeField(auto_now_add=True, verbose_name="更新日時")
    is_deleted = models.BooleanField(default=False, verbose_name="削除フラグ")

    class Meta:
        abstract = True
        verbose_name_plural = "ベースモデル"
        db_table = "BaseTable"
