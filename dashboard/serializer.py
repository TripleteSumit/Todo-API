from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.serializers import ValidationError
from .models import Task, SubTask


class SubTaskSerializer(ModelSerializer):
    class Meta:
        model = SubTask
        exclude = ["created_at", "updated_at"]

    def validate(self, data):
        given_data = self.initial_data
        expected_keys = ["steps", "is_complete"]
        unexpected_keys = []
        error = []

        for key in given_data.keys():
            if key not in expected_keys:
                unexpected_keys.append(key)

        if unexpected_keys:
            error.append({"unexpected_keys": unexpected_keys})

        if error:
            raise ValidationError({"error": error})

        return data

    def create(self, validated_data):
        task_id = self.context.get("task_id")
        return SubTask.objects.create(task_id=task_id, **validated_data)

    def update(self, instance, validated_data):
        if not instance.is_complete and validated_data.get("is_complete"):
            instance.task.total_subtask_completed = (
                instance.task.total_subtask_completed + 1
            )
            instance.task.save()
        elif instance.is_complete and not validated_data.get("is_complete"):
            instance.task.total_subtask_completed = (
                instance.task.total_subtask_completed - 1
            )
            instance.task.save()

        return super().update(instance, validated_data)


class TaskSerializer(ModelSerializer):
    subtask = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "attachment",
            "is_important",
            "status",
            "subtask",
            "total_subtask",
            "total_subtask_completed",
        )

    def validate(self, data):
        given_date = self.initial_data
        required_data = ["title"]
        expected_data = ["title", "description", "attachment", "is_important", "status"]
        error = []
        unexpected_keys = []
        required_keys = []

        for key in required_data:
            if key not in given_date.keys():
                required_keys.append(key)

        for key in given_date.keys():
            if key not in expected_data:
                unexpected_keys.append(key)

        if required_keys:
            error.append({"required_keys": required_keys})

        if unexpected_keys:
            error.append({"unexpected_keys": unexpected_keys})

        if error:
            raise ValidationError({"error": error})

        return data

    def create(self, validated_data):
        user = self.context.get("user")
        return Task.objects.create(user=user, **validated_data)
