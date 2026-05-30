from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import StudentProfile


@login_required
def student_profile_list(request):
    profiles = StudentProfile.objects.select_related('user')
    return render(request, 'simple/list.html', {
        'title': 'Student Profiles',
        'headers': ['Name', 'Roll Number', 'Course', 'Semester'],
        'rows': [[item.user.get_full_name() or item.user.username, item.roll_number, item.course, item.semester] for item in profiles],
    })
