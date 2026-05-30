from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import PlacementOpportunity


@login_required
def placement_list(request):
    opportunities = PlacementOpportunity.objects.all()
    return render(request, 'simple/list.html', {
        'title': 'Placements',
        'headers': ['Company', 'Job Title', 'Package', 'Last Date'],
        'rows': [[item.company_name, item.job_title, item.package, item.last_date] for item in opportunities],
    })
