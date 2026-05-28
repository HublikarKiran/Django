from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile


class EnterpriseUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'created_at')
    list_filter = ('role', 'is_verified', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone_number',
                     'first_name', 'last_name')
    ordering = ('created_at',)

    fieldsets = UserAdmin.fieldsets + (
        "Enterprise Profile",
        {
            'fields': (
                'role',
                'phone_number',
                'profile_picture',
                'is_verified',
            )
        },
        ("Audit", {"fields": ("created_at", "updated_at")})
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number', 'course', 'semester')
    list_filter = ('course', 'semester')
    search_fields = ('user__username', 'user__email', 'roll_number', 'course')
    ordering = ('user__created_at',)
