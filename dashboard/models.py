from django.db import models
from core.models import User
from .signal import (
    update_task_status_post_delete_signal,
    update_task_status_post_save_signal,
)
from django.db.models.signals import post_save, post_delete


# Create your models here.
class Task(models.Model):
    TASK_STATUS = (
        ("todo", "Todo"),
        ("progress", "Progress"),
        ("done", "Done"),
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="task", blank=True
    )
    title = models.CharField(max_length=255, blank=True)
    description = models.CharField(
        verbose_name="Note", max_length=255, null=True, blank=True
    )
    attachment = models.FileField(upload_to="attachments", null=True, blank=True)
    is_important = models.BooleanField(default=False)
    status = models.CharField(
        max_length=10, choices=TASK_STATUS, default="todo", blank=True
    )
    total_subtask = models.SmallIntegerField(blank=True, default=0)
    total_subtask_completed = models.SmallIntegerField(blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SubTask(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, blank=True, related_name="subtask"
    )
    steps = models.CharField(max_length=255)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


post_save.connect(receiver=update_task_status_post_save_signal, sender=SubTask)
post_delete.connect(receiver=update_task_status_post_delete_signal, sender=SubTask)
