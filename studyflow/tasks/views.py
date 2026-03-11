from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskSerializer
from django.utils import timezone
from datetime import timedelta


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # 🔹 Today's Tasks
    @action(detail=False, methods=['get'])
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
    @action(detail=False, methods=['get'])
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
    


class SubTaskViewSet(viewsets.ModelViewSet):
    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SubTask.objects.filter(task__user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save()