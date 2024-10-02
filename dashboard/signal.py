def update_task_status_post_save_signal(sender, instance, created, **kwargs):
    from .models import Task
    from django.db.models import F

    if created:
        Task.objects.filter(subtask=instance).update(
            total_subtask=F("total_subtask") + 1
        )


def update_task_status_post_delete_signal(sender, instance, **kwargs):
    from .models import Task
    from django.db.models import F


    Task.objects.filter(subtask=instance).update(
    total_subtask=F("total_subtask") - 1
    )
