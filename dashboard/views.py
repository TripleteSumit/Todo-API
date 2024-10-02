from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from django.http import Http404
from rest_framework import status
from .serializer import TaskSerializer, SubTaskSerializer
from .models import Task, SubTask


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete", "options", "head"]

    def get_queryset(self):
        status = self.request.query_params.get("status")
        if status and status not in ["todo", "progress", "done"]:
            raise serializers.ValidationError(
                {"status": "Invalid status. Valid statuses are [todo, progress, done]"}
            )

        queryset = Task.objects.filter(user=self.request.user).order_by(
            "-is_important", "status"
        )
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_serializer_context(self):
        return {"user": self.request.user}

    def list(self, request, *args, **kwargs):
        response_data = super().list(request, *args, **kwargs)

        response = {}
        if response_data.data:
            response["status"] = "success"
            response["message"] = "Successfully retrieve the task."
        else:
            response["status"] = "failed"
            response["message"] = "No data found."

        response["data"] = response_data.data
        return Response(response, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, *args, **kwargs)

            if response.data:
                custom_response = {
                    "status": "success",
                    "message": "Successfully retrieve the task.",
                    "data": response.data,
                }
                return Response(custom_response, status=status.HTTP_404_NOT_FOUND)
            return response
        except Http404:
            custom_response = {"status": "failed", "message": "Invalid task id"}
            return Response(custom_response, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        if response.data:
            custom_response = {
                "status": "success",
                "message": "Successfully created the task.",
                "data": response.data,
            }
            return Response(custom_response, status=status.HTTP_201_CREATED)
        return response

    def partial_update(self, request, *args, **kwargs):
        try:
            response = super().partial_update(request, *args, **kwargs)

            if response.data:
                custom_response = {
                    "status": "success",
                    "message": "Successfully updated the task.",
                    "data": response.data,
                }
                return Response(custom_response, status=status.HTTP_200_OK)
            return response
        except Http404:
            custom_response = {
                "status": "failed",
                "message": "Invalid task id",
            }
            return Response(custom_response, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            if SubTask.objects.filter(task_id=self.kwargs["pk"]).count() > 0:
                return Response(
                    {
                        "status": "failed",
                        "message": "Task cannnot be deleted because it associated with multiple subtasks",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return super().destroy(request, *args, **kwargs)
        except Http404:
            custom_response = {
                "status": "failed",
                "message": "Invalid task id",
            }
            return Response(custom_response, status=status.HTTP_404_NOT_FOUND)


class SubTaskViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubTaskSerializer
    http_method_names = ["get", "post", "patch", "options", "head", "delete"]

    def update_task_status(self, task_id):
        subtask_qs = SubTask.objects.filter(task_id=task_id, is_complete=True)
        task = subtask_qs.first().task if subtask_qs.exists() else None

        if task:
            count = subtask_qs.count()
            if count > 0:
                task.status = "progress"
            elif count == 0:
                task.status = "todo"
            task.save()

    def get_queryset(self):
        task_id = self.kwargs["task_pk"]
        queryset = SubTask.objects.filter(task_id=task_id).order_by("is_complete")
        return queryset

    def get_serializer_context(self):
        return {"task_id": self.kwargs["task_pk"]}

    def list(self, request, *args, **kwargs):
        response_data = super().list(request, *args, **kwargs)

        response = {}
        if response_data.data:
            response["status"] = "success"
            response["message"] = "Successfully retrieve the subtask."
        else:
            response["status"] = "failed"
            response["message"] = "No data found."

        response["data"] = response_data.data
        return Response(response, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, *args, **kwargs)
            if response.data:
                custom_response = {
                    "status": "success",
                    "message": "Successfully retrieve the subtask.",
                    "data": response.data,
                }
                return Response(custom_response, status=status.HTTP_404_NOT_FOUND)
            return response
        except Http404:
            custom_response = {"status": "failed", "message": "Invalid subtask id"}
            return Response(custom_response, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        self.update_task_status(self.kwargs["task_pk"])

        if response.data:
            custom_response = {
                "status": "success",
                "message": "Successfully created the subtask.",
                "data": response.data,
            }
            return Response(custom_response, status=status.HTTP_201_CREATED)
        return response

    def partial_update(self, request, *args, **kwargs):
        try:
            response = super().partial_update(request, *args, **kwargs)
            self.update_task_status(self.kwargs["task_pk"])

            if response.data:
                custom_response = {
                    "status": "success",
                    "message": "Successfully updated the subtask.",
                    "data": response.data,
                }
                return Response(custom_response, status=status.HTTP_200_OK)
            return response
        except Http404:
            custom_response = {
                "status": "failed",
                "message": "Invalid subtask id",
            }
            return Response(custom_response, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
            self.update_task_status(self.kwargs["task_pk"])
            return response
        except Http404:
            custom_response = {
                "status": "failed",
                "message": "Invalid subtask id",
            }
            return Response(custom_response, status=status.HTTP_404_NOT_FOUND)
