from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TaskModel(models.Model):
    task_type = models.CharField(max_length=100, choices=(('allow_user', "启用用户"), ('forbidden_user', "禁用用户")))
    server_use = models.ForeignKey("server.ServerModel", on_delete=models.CASCADE, verbose_name="使用情况", related_name="belongs_to")
    expect_exec_time = models.DateTimeField(verbose_name="预期执行时间")
    actual_exec_time = models.DateTimeField(verbose_name="实际执行完成时间")
    has_exec = models.BooleanField(default=False, verbose_name="已经执行")
