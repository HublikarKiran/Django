from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import AdmissionApplication


@login_required
def admission_list(request):
    applications = AdmissionApplication.objects.all()
    return render(request, 'simple/list.html', {
        'title': 'Admissions',
        'headers': ['Applicant', 'Email', 'Course', 'Status'],
        'rows': [[item.applicant_name, item.email, item.course, item.status] for item in applications],
    })
