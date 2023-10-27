from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ServerModel(models.Model):
    class Meta:
        db_table = "server_model"
        verbose_name = "服务器"
        verbose_name_plural = verbose_name

    name = models.CharField(max_length=30, verbose_name="服务器名称")
    addr = models.CharField(max_length=30, verbose_name="服务器地址")
    desc = models.CharField(max_length=200, verbose_name="服务器描述")

    def __str__(self):
        return str(self.name)


class ServerUseModel(models.Model):
    class Meta:
        db_table = "server_use_model"
        verbose_name = "服务器使用情况"
        verbose_name_plural = verbose_name

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户", related_name="has_servers",
                             db_index=True)

    server = models.ForeignKey(ServerModel, on_delete=models.CASCADE, verbose_name="服务器")
    public_key = models.CharField(max_length=500, verbose_name="公钥")
    start_time = models.DateTimeField(verbose_name="开始时间")
    end_time = models.DateTimeField(verbose_name="结束时间")
    can_use = models.BooleanField(verbose_name="有效")
    status = models.CharField(
        max_length=20,
        choices=(('creating', "创建中"), ('using', "使用中"), ('end', "使用结束")))

    def __str__(self):
        return f"{self.user.first_name}-{self.server.name}"
