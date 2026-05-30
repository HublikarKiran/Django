from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Roles(models.TextChoices):
        SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin'
        STUDENT = 'STUDENT', 'Student'
        FACULTY = 'FACULTY', 'Faculty'
        ADMIN = 'ADMIN', 'Admin'
        PARENT = 'PARENT', 'Parent'

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=30, choices=Roles.choices, default=Roles.STUDENT)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_admin_role(self):
        return self.role in [self.Roles.ADMIN, self.Roles.SUPER_ADMIN] or self.is_superuser

    def __str__(self):
        return f"{self.get_full_name() or self.username}  ({self.role})"


class StudentProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=20, unique=True)
    course = models.CharField(max_length=100)
    semester = models.CharField(max_length=20)
    skills = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.roll_number}"
