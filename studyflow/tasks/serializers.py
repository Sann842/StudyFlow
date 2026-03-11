from rest_framework import serializers
from .models import Task, SubTask
from holidays.models import Holiday

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

    def get_is_holiday(self, obj):
        """Check if the task’s due date falls on a holiday."""
        return Holiday.objects.filter(date=obj.due_date.date()).exists()



class SubTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubTask
        fields = ['id', 'task', 'title', 'is_completed', 'created_at']
        read_only_fields = ['id', 'created_at']