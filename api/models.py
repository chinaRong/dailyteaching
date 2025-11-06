from django.db import models
from django.contrib.postgres.fields import JSONField  # 若用 PostgreSQL


# 对于 SQLite / MySQL / 默认情况，可直接用 models.JSONField

class UserData(models.Model):
    """
    用户访问数据表：
      - user_id：来自 NFC 手环的网址参数
      - data_map：JSON 格式的用户访问数据（例如每日访问记录）
      - created_at：创建时间
      - updated_at：最后更新时间
    """

    user_id = models.CharField(max_length=64, unique=True, db_index=True)
    data_map = models.JSONField(default=dict)  # Django 3.1+ 内置支持 JSONField
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"UserData<{self.user_id}>"

    class Meta:
        db_table = "user_data"
        verbose_name = "用户访问数据"
        verbose_name_plural = "用户访问数据表"
