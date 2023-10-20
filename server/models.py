from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils import timezone
from scheduler.sheduler import global_sheduler

from task.models import TaskModel


# Create your models here.
class ServerModel(models.Model):
    class Meta:
        db_table = "server_model"
        verbose_name = "服务器"
        verbose_name_plural = verbose_name

    name = models.CharField(max_length=30, verbose_name="服务器名称", db_index=True)
    addr = models.CharField(max_length=30, verbose_name="服务器地址", db_index=True)

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
    status = models.CharField(
        max_length=20,
        choices=(('creating', "创建中"), ('using', "使用中"), ('end', "使用结束")))


def handle_use(sender, instance, created, **kwargs):
    if created:
        TaskModel.objects.create(
            task_type="allow_user",
            server_use=instance,
            expect_exec_time=timezone.now()
        )
        TaskModel.objects.create(
            task_type="forbidden_user",
            server_use=instance,
            expect_exec_time=timezone.now()
        )

    else:
        task = TaskModel.objects.filter(server_use=instance,task_type="forbidden_user").first()
        task.expect_exec_time = instance.end_time()

    global_sheduler.wakeup()


post_save.connect(handle_use, sender=ServerUseModel)
