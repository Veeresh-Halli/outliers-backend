


def is_permission_allowed(task_instance, user):
    return True if task_instance.user == user else False
