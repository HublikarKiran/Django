from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import User
from .models import AttendanceRecord


@login_required
def attendance_list(request):
    records = AttendanceRecord.objects.select_related('student', 'subject')
    if request.user.role == User.Roles.STUDENT:
        records = records.filter(student=request.user)
    return render(request, 'simple/list.html', {
        'title': 'Attendance',
        'headers': ['Student', 'Subject', 'Date', 'Status', 'Remarks'],
        'rows': [[item.student.username, item.subject.code, item.date, item.status, item.remarks] for item in records],
    })
