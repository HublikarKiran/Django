from django.urls import path

from . import views

app_name = 'attendence'

urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),
]
