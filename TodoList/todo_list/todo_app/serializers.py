from rest_framework import serializers

from todo_app.models import Task


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ("user",)
