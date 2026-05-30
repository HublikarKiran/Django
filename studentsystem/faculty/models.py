from django.db import models
from django.conf import settings


class FacultyProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='faculty_profile')
    employee_id = models.CharField(max_length=30, unique=True)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.department}"
