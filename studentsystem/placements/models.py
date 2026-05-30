from django.db import models
from django.conf import settings


class PlacementOpportunity(models.Model):
    company_name = models.CharField(max_length=150)
    job_title = models.CharField(max_length=150)
    description = models.TextField()
    package = models.CharField(max_length=100, blank=True)
    last_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_date']

    def __str__(self):
        return f"{self.company_name} - {self.job_title}"


class PlacementApplication(models.Model):
    opportunity = models.ForeignKey(PlacementOpportunity, on_delete=models.CASCADE, related_name='applications')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='placement_applications')
    status = models.CharField(max_length=40, default='Applied')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('opportunity', 'student')

    def __str__(self):
        return f"{self.student.username} - {self.opportunity}"
