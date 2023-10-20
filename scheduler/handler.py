from task.models import TaskModel

def task_handler(task:TaskModel):
    task_type = task.task_type
    username = task.server_use.user
    pass


def allow_user(username, server_addr):
    pass


def forbidden_user(username, server_addr):
    pass
