from rest_framework import serializers
from todoapp.models import Todos


class TodoSerializer(serializers.ModelSerializer):
    completed_status = serializers.CharField(read_only=True)

    class Meta:
        model = Todos

    fields = [
        "task_name",
        "user",
        "completed_status"
    ]
