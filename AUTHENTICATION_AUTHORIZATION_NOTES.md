# Authentication And Authorization Notes

## Authentication vs Authorization

Authentication means identifying who the user is.

Example:

```text
Is this request from kiran?
```

Authorization means deciding what that user is allowed to do.

Example:

```text
Can kiran delete a student record?
```

## Where Authentication Is Configured

Main settings file:

```text
studentsystem/studentsystem/settings.py
```

Installed Django auth apps:

```python
'django.contrib.auth',
'django.contrib.sessions',
```

Authentication middleware:

```python
'django.contrib.sessions.middleware.SessionMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
```

Custom user model:

```python
AUTH_USER_MODEL = 'accounts.User'
```

Login URLs:

```python
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'accounts:dashboard'
LOGOUT_REDIRECT_URL = 'accounts:login'
```

## Custom User Model

Configured in:

```text
studentsystem/accounts/models.py
```

The custom user extends:

```python
AbstractUser
```

Extra fields include:

```text
role
phone_number
profile_picture
is_verified
created_at
updated_at
```

Roles:

```python
SUPER_ADMIN
STUDENT
FACULTY
ADMIN
PARENT
```

Admin check:

```python
def is_admin_role(self):
    return self.role in [self.Roles.ADMIN, self.Roles.SUPER_ADMIN] or self.is_superuser
```

## Web Login

Configured in:

```text
studentsystem/accounts/views.py
```

Login view:

```python
def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('accounts:dashboard')
```

`login(request, user)` creates the session for the authenticated user.

Login route:

```text
/accounts/login/
```

Configured in:

```text
studentsystem/accounts/urls.py
```

## Web Logout

Configured in:

```text
studentsystem/accounts/views.py
```

Logout view:

```python
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')
```

Logout route:

```text
/accounts/logout/
```

## Web Authorization

Many Django web views use:

```python
@login_required
```

Example:

```python
@login_required
def student_dashboard(request):
    ...
```

Admin-only access is handled with:

```python
def admin_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin_role():
            messages.error(request, 'Admin access is required.')
            return redirect('accounts:student_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper
```

## Role-Based Authorization Decorator

Configured in:

```text
studentsystem/accounts/decorators.py
```

Code:

```python
def role_required(*roles):
    ...
```

This decorator checks:

```python
if request.user.role not in roles:
    raise PermissionDenied
```

Note: in the current code, this decorator is available but not widely used.

## DRF Authentication

Configured in:

```text
studentsystem/studentsystem/settings.py
```

Current DRF authentication:

```python
DEFAULT_AUTHENTICATION_CLASSES = [
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication',
]
```

Meaning:

- browser API requests can use Django sessions
- tools like curl/Postman can use Basic Auth

## DRF Authorization

Global default:

```python
DEFAULT_PERMISSION_CLASSES = [
    'rest_framework.permissions.IsAuthenticated',
]
```

So API endpoints require authentication unless a view overrides permissions.

Example public endpoint:

```python
@permission_classes([permissions.AllowAny])
def health(request):
    ...
```

Route:

```text
GET /api/health/
```

## Custom API Permission Classes

Configured in:

```text
studentsystem/api/views.py
```

### AdminOnlyPermission

Code:

```python
class AdminOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin_role()
```

Used by:

```python
UserViewSet
```

Meaning:

Only admins can access user APIs.

### AdminWritePermission

Code:

```python
class AdminWritePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.is_admin_role()
```

Meaning:

- authenticated users can read
- only admins can create, update, or delete

Used by many API viewsets, including subjects, materials, assignments, attendance, results, notifications, placements, admissions, faculty profiles, and parent profiles.

## Current Authentication Summary

Currently configured:

- Django session login for the web app
- DRF session authentication
- DRF basic authentication
- role-based authorization using the custom `User.role`
- admin authorization using `is_admin_role()`

Not currently configured:

- DRF token authentication
- JWT authentication

