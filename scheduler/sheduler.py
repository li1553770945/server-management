import logging
from datetime import timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.util import timedelta_seconds
from django.utils import timezone
from django.db import transaction
from task.models import TaskModel

logger = logging.getLogger(__name__)



class TaskScheduler(BackgroundScheduler):
    misfire_grace_time = 60
    MAX_WAIT_TIME = 60 * 60  # wake up every hour

    def _process_jobs(self):
        logger.info('调度器被唤醒')
        try:
            now = timezone.now()
            grace_time = timedelta(seconds=self.misfire_grace_time)

            with self._jobstores_lock:
                with transaction.atomic():

                    task_list = list(TaskModel.objects.select_for_update().filter(
                        has_exec=False, expect_exec_time__range=(now - grace_time, now)).all())
                    for task in task_list:
                        # TODO: 业务逻辑没写
                        task.actual_exec_time = timezone.now()
                        task.has_exec = True
                        task.save()

                    next_task = TaskModel.objects.filter(
                        has_exec=False, expect_exec_time__gt=now - grace_time).order_by('expect_exec_time').first()
                    if next_task:
                        wait_seconds = max(timedelta_seconds(next_task - timezone.now()), 0)
                        logger.info('下次调度器唤醒时间 %s (in %f seconds)', next_task.expect_exec_time.isoformat(),
                                    wait_seconds)
                        return wait_seconds
                    else:
                        logger.info('没有待完成的工作，调度器休眠')
                        return None
        except Exception as e:
            logger.exception('调度器发生异常')


global_sheduler = BackgroundScheduler()
