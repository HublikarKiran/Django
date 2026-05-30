from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Notification


@login_required
def notification_list(request):
    notifications = Notification.objects.filter(recipient__isnull=True) | Notification.objects.filter(recipient=request.user)
    return render(request, 'simple/list.html', {
        'title': 'Notifications',
        'headers': ['Title', 'Message', 'Created'],
        'rows': [[item.title, item.message, item.created_at] for item in notifications],
    })
