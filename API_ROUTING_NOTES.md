# API Routing Notes

## What API Routing Means

API routing connects a URL to a view. When a request comes in, Django checks `urlpatterns` and sends the request to the matching view.

In this project, API routing has two levels:

- project-level routing in `studentsystem/studentsystem/urls.py`
- API-app routing in `studentsystem/api/urls.py`

## Project-Level API Route

Configured in:

```text
studentsystem/studentsystem/urls.py
```

Code:

```python
path('api/', include('api.urls')),
```

This means all API URLs begin with:

```text
/api/
```

## API-App Routes

Configured in:

```text
studentsystem/api/urls.py
```

Important imports:

```python
from django.urls import include, path
from rest_framework.routers import DefaultRouter
```

Router setup:

```python
router = DefaultRouter()
```

Then viewsets are registered:

```python
router.register('subjects', views.SubjectViewSet)
```

Finally router URLs are included:

```python
path('', include(router.urls)),
```

## Why DefaultRouter Is Used

`DefaultRouter` automatically creates RESTful routes for each registered viewset.

For example:

```python
router.register('subjects', views.SubjectViewSet)
```

Creates:

```text
GET    /api/subjects/
POST   /api/subjects/
GET    /api/subjects/{id}/
PUT    /api/subjects/{id}/
PATCH  /api/subjects/{id}/
DELETE /api/subjects/{id}/
```

## Registered API Routes In This Project

Configured in:

```text
studentsystem/api/urls.py
```

```python
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
```

## Why basename Is Used For Some Routes

Routes like this use `basename`:

```python
router.register('submissions', views.AssignmentSubmissionViewSet, basename='submissions')
router.register('chat-messages', views.ChatMessageViewSet, basename='chat-messages')
```

This is because those viewsets do not define a fixed class-level `queryset`. Instead, they use `get_queryset()` so results can depend on the current user.

DRF needs `basename` to name the generated URL patterns when there is no fixed `queryset`.

## Function-Based API Route

This project also has a manual API route:

```python
path('health/', views.health, name='api_health')
```

Full URL:

```text
GET /api/health/
```

View location:

```text
studentsystem/api/views.py
```

## API Routing Flow

Example request:

```text
GET /api/subjects/
```

Flow:

1. Django enters `studentsystem/studentsystem/urls.py`.
2. It matches `api/`.
3. Django includes `studentsystem/api/urls.py`.
4. DRF `DefaultRouter` matches `subjects/`.
5. The request is handled by `SubjectViewSet`.
6. `SubjectSerializer` converts model data to JSON.
7. DRF returns a JSON response.

## Web Routes vs API Routes

Web routes return HTML templates.

Example:

```text
/accounts/login/
/chatbot/
/learning/
```

API routes return JSON data.

Example:

```text
/api/users/
/api/subjects/
/api/chat-messages/
```

