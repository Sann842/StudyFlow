from django.db import models
from django.conf import settings
from courses.models import Course

class Task(models.Model):

    TASK_TYPE_CHOICES = [
        ('assignment', 'Assignment'),
        ('exam', 'Exam'),
        ('project', 'Project'),
        ('homework', 'Homework'),
        ('self_study', 'Self Study'),
        ('group_work', 'Group Work'),
        ('general', 'General'),
    ]


    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    task_type = models.CharField(
        max_length=20,
        choices=TASK_TYPE_CHOICES,
        default='assignment'
    )

    due_date = models.DateTimeField()

    estimated_hours = models.FloatField(default=1)

    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=2
    )

    is_completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return self.title



class SubTask(models.Model):

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='subtasks'
    )

    title = models.CharField(max_length=255)

    is_completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title