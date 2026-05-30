from django.db import models
from django.conf import settings


class Result(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey('learning.Subject', on_delete=models.CASCADE, related_name='results')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    grade = models.CharField(max_length=10, blank=True)
    exam_name = models.CharField(max_length=100, default='Semester Exam')
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return f"{self.student.username} - {self.subject.code} - {self.grade}"
