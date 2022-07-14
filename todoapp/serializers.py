from rest_framework import serializers
from todoapp.models import Todos
from django.contrib.auth.models import User


class TodoSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    completed_status = serializers.CharField(read_only=True)

    class Meta:
        model = Todos
        fields = [
            "id",
            "task_name",
            "completed_status"
        ]
    def create(self, validated_data):
        user=self.context.get("user")
        return Todos.objects.create(**validated_data,user=user)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password"
        ]

    def create(self, validated_data):
        print(validated_data)
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

