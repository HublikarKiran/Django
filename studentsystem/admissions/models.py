from django.db import models
from django.conf import settings


class AdmissionApplication(models.Model):
    STATUS_CHOICES = (
        ('NEW', 'New'),
        ('REVIEWING', 'Reviewing'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    applicant_name = models.CharField(max_length=150)
    email = models.EmailField()
    course = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    handled_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.applicant_name} - {self.course}"
