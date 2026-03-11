from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskSerializer
from django.utils import timezone
from datetime import timedelta, date


class TaskViewSet(viewsets.ModelViewSet):
    """
    TaskViewSet handles:
    - CRUD: list, create, retrieve, update, delete
    - Today tasks
    - Upcoming tasks (next 7 days)
    - Smart priority ranking
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # 🔹 Today's Tasks
    @action(detail=False, methods=['get'], url_path='today')
    def today(self, request):
        today = timezone.now().date()
        tasks = Task.objects.filter(
            user=request.user,
            due_date__date=today,
            is_completed=False
        )
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    # 🔹 Upcoming Tasks (Next 7 days)
    @action(detail=False, methods=['get'], url_path='upcoming')
    def upcoming(self, request):
        today = timezone.now()
        next_week = today + timedelta(days=7)
        tasks = Task.objects.filter(
            user=request.user,
            due_date__range=[today, next_week],
            is_completed=False
        ).order_by('due_date')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)
    

    # 🔹 Smart Priority Ranking
    @action(detail=False, methods=['get'], url_path='smart-priority')
    def smart_priority(self, request):
        tasks = Task.objects.filter(
            user=request.user,
            is_completed=False
        )
        ranked_tasks = []
        today = date.today()

        for task in tasks:
            days_left = (task.due_date.date() - today).days
            if days_left < 0:
                days_left = 0

            urgency_score = 10 / (days_left + 1)
            priority_score = task.priority * 2
            workload_score = task.estimated_hours / 2

            final_score = urgency_score + priority_score + workload_score

            ranked_tasks.append({
                "task": task,
                "score": final_score
            })

        # Sort descending by score
        ranked_tasks.sort(key=lambda x: x["score"], reverse=True)
        sorted_tasks = [item["task"] for item in ranked_tasks]

        serializer = self.get_serializer(sorted_tasks, many=True)
        return Response(serializer.data)
    


class SubTaskViewSet(viewsets.ModelViewSet):
    """
    SubTaskViewSet handles:
    - CRUD: list, create, retrieve, update, delete
    - All actions restricted to the authenticated user's tasks
    """
    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SubTask.objects.filter(task__user=self.request.user)
    
    def perform_create(self, serializer):
        # Ensure task belongs to user
        task = serializer.validated_data['task']
        if task.user != self.request.user:
            raise PermissionError("Cannot add a subtask to another user's task")
        serializer.save()