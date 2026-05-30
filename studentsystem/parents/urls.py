from django.urls import path

from . import views

app_name = 'parents'

urlpatterns = [
    path('', views.parent_list, name='parent_list'),
]
