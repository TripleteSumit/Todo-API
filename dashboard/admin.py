from django.contrib import admin
from .models import Task, SubTask


class TaskAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]


admin.site.register(Task, TaskAdmin)
