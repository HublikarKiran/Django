from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import ParentProfile


@login_required
def parent_list(request):
    profiles = ParentProfile.objects.select_related('user', 'student')
    return render(request, 'simple/list.html', {
        'title': 'Parents',
        'headers': ['Parent', 'Student', 'Relation'],
        'rows': [[item.user.get_full_name() or item.user.username, item.student.get_full_name() or item.student.username, item.relation] for item in profiles],
    })
