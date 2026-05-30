from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('student-profiles', views.StudentProfileViewSet)
router.register('subjects', views.SubjectViewSet)
router.register('materials', views.StudyMaterialsViewSet)
router.register('assignments', views.AssignmentViewSet)
router.register('submissions', views.AssignmentSubmissionViewSet, basename='submissions')
router.register('chat-messages', views.ChatMessageViewSet, basename='chat-messages')
router.register('attendance', views.AttendanceRecordViewSet)
router.register('results', views.ResultViewSet)
router.register('notifications', views.NotificationViewSet)
router.register('placement-opportunities', views.PlacementOpportunityViewSet)
router.register('placement-applications', views.PlacementApplicationViewSet)
router.register('admissions', views.AdmissionApplicationViewSet)
router.register('faculty-profiles', views.FacultyProfileViewSet)
router.register('parent-profiles', views.ParentProfileViewSet)

urlpatterns = [
    path('health/', views.health, name='api_health'),
    path('', include(router.urls)),
]
