from django.contrib.auth.models import User
from django.db import models


class UserInfoModel(models.Model):
    class Meta:
        db_table = "user_info"
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户", related_name="user_info",
                             db_index=True)
    year = models.IntegerField(verbose_name="入学年份")

    def __str__(self):
        return str(self.user.first_name)
