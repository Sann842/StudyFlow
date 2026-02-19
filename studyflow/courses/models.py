from django.db import models
from django.conf import settings

class Course(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    semester = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'code')  # Prevent duplicate course codes per user

    def __str__(self):
        return f"{self.name} ({self.code})"
