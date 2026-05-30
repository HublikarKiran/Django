from django.urls import path
from django.shortcuts import redirect

app_name = 'assignments'

urlpatterns = [
    path('', lambda request: redirect('learning:assignment_list'), name='assignment_list'),
]
