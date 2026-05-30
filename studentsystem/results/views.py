from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import User
from .models import Result


@login_required
def result_list(request):
    results = Result.objects.select_related('student', 'subject')
    if request.user.role == User.Roles.STUDENT:
        results = results.filter(student=request.user)
    return render(request, 'simple/list.html', {
        'title': 'Results',
        'headers': ['Student', 'Subject', 'Exam', 'Marks', 'Grade'],
        'rows': [[item.student.username, item.subject.code, item.exam_name, f'{item.marks_obtained}/{item.max_marks}', item.grade] for item in results],
    })
