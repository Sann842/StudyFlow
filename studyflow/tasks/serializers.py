from rest_framework import serializers
from .models import Task, SubTask

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [
            'id',
            'course',
            'title',
            'description',
            'task_type',
            'due_date',
            'estimated_hours',
            'priority',
            'is_completed',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']



class SubTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubTask
        fields = ['id', 'task', 'title', 'is_completed', 'created_at']
        read_only_fields = ['id', 'created_at']