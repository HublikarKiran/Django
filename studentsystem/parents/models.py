from django.db import models
from django.conf import settings


class ParentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='parent_profile')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='parent_profiles')
    relation = models.CharField(max_length=50, default='Parent')
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} parent of {self.student.username}"
