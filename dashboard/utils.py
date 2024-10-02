def get_boolean(data, key):
    return True if (data.get(key)).lower() == "true" else False


def set_total_subtask():
    from .models import Task

    tasks = Task.objects.prefetch_related("subtask").all()

    for task in tasks:
        subtask = getattr(task, "subtask", None)
        # if subtask:
        task.total_subtask_completed = task.subtask.filter(is_complete=True).count()
        # else:
        # task.total_subtask = 0

        task.save()
