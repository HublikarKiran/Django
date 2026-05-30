"""
URL configuration for studentsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from accounts import views as account_views

urlpatterns = [
    path('', account_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('learning/', include('learning.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('student/', include('student.urls')),
    path('faculty/', include('faculty.urls')),
    path('parents/', include('parents.urls')),
    path('attendence/', include('attendence.urls')),
    path('notifications/', include('notifications.urls')),
    path('placements/', include('placements.urls')),
    path('assignments/', include('assignments.urls')),
    path('admissions/', include('admissions.urls')),
    path('results/', include('results.urls')),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
