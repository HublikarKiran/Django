from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import FacultyProfile


@login_required
def faculty_list(request):
    profiles = FacultyProfile.objects.select_related('user')
    return render(request, 'simple/list.html', {
        'title': 'Faculty',
        'headers': ['Name', 'Employee ID', 'Department', 'Designation'],
        'rows': [[item.user.get_full_name() or item.user.username, item.employee_id, item.department, item.designation] for item in profiles],
    })
