from django.db import models

# Create your models here.
from django.conf import settings


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name="subjects_created")

    def __str__(self):
        return f"{self.name} - {self.code})"

class StudyMaterials(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="materials")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='study_materials/')
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
        null=True, related_name="materials_uploaded")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return self.title
    
class Assignment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="assignments")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file= models.FileField(upload_to='assignments/', blank=True, null=True)
    due_date = models.DateTimeField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
        null=True, related_name="assignments_created")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['due_date']
    def __str__(self):
        return self.title
    

class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
        related_name="assignment_submissions")
    answer_text = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='assignment_submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=10, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('assignment', 'student')
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.student.username} -> {self.assignment.title}"