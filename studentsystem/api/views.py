from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from accounts.models import StudentProfile, User
from admissions.models import AdmissionApplication
from attendence.models import AttendanceRecord
from chatbot.models import ChatMessage
from chatbot.views import build_study_answer
from faculty.models import FacultyProfile
from learning.models import Assignment, AssignmentSubmission, StudyMaterials, Subject
from notifications.models import Notification
from parents.models import ParentProfile
from placements.models import PlacementApplication, PlacementOpportunity
from results.models import Result

from .serializers import (
    AdmissionApplicationSerializer,
    AssignmentSerializer,
    AssignmentSubmissionSerializer,
    AttendanceRecordSerializer,
    ChatMessageSerializer,
    FacultyProfileSerializer,
    NotificationSerializer,
    ParentProfileSerializer,
    PlacementApplicationSerializer,
    PlacementOpportunitySerializer,
    ResultSerializer,
    StudentProfileSerializer,
    StudyMaterialsSerializer,
    SubjectSerializer,
    UserSerializer,
)


class AdminWritePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.is_admin_role()


class AdminOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin_role()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [AdminOnlyPermission]


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.select_related('user').all()
    serializer_class = StudentProfileSerializer
    permission_classes = [AdminWritePermission]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all().order_by('name')
    serializer_class = SubjectSerializer
    permission_classes = [AdminWritePermission]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class StudyMaterialsViewSet(viewsets.ModelViewSet):
    queryset = StudyMaterials.objects.select_related('subject').all()
    serializer_class = StudyMaterialsSerializer
    permission_classes = [AdminWritePermission]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.select_related('subject').all()
    serializer_class = AssignmentSerializer
    permission_classes = [AdminWritePermission]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = AssignmentSubmission.objects.select_related('assignment', 'student')
        if self.request.user.is_admin_role():
            return queryset
        return queryset.filter(student=self.request.user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_admin_role():
            return ChatMessage.objects.all()
        return ChatMessage.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        question = serializer.validated_data.get('question')
        serializer.save(user=self.request.user, answer=build_study_answer(question))


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.select_related('student', 'subject').all()
    serializer_class = AttendanceRecordSerializer
    permission_classes = [AdminWritePermission]


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.select_related('student', 'subject').all()
    serializer_class = ResultSerializer
    permission_classes = [AdminWritePermission]


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [AdminWritePermission]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PlacementOpportunityViewSet(viewsets.ModelViewSet):
    queryset = PlacementOpportunity.objects.all()
    serializer_class = PlacementOpportunitySerializer
    permission_classes = [AdminWritePermission]


class PlacementApplicationViewSet(viewsets.ModelViewSet):
    queryset = PlacementApplication.objects.select_related('opportunity', 'student').all()
    serializer_class = PlacementApplicationSerializer
    permission_classes = [AdminWritePermission]


class AdmissionApplicationViewSet(viewsets.ModelViewSet):
    queryset = AdmissionApplication.objects.all()
    serializer_class = AdmissionApplicationSerializer
    permission_classes = [AdminWritePermission]


class FacultyProfileViewSet(viewsets.ModelViewSet):
    queryset = FacultyProfile.objects.select_related('user').all()
    serializer_class = FacultyProfileSerializer
    permission_classes = [AdminWritePermission]


class ParentProfileViewSet(viewsets.ModelViewSet):
    queryset = ParentProfile.objects.select_related('user', 'student').all()
    serializer_class = ParentProfileSerializer
    permission_classes = [AdminWritePermission]


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health(request):
    return Response({'status': 'ok'})
