# Security Guide for the Student Management System

This guide explains the security model used in this Django project in a clear, beginner-friendly, lecture-style way.

The most important idea is this:

This project is not using JWT authentication. It is not using custom API tokens. It is not using hand-written token logic. Instead, it uses Django's built-in authentication system, Django's built-in session framework for browser login, Django REST Framework permissions for API access, role-based authorization, CSRF protection, password hashing, form validation, and Django ORM protections.

Think of the project security as a university building:

- Authentication answers: "Who are you?"
- Authorization answers: "What are you allowed to do?"
- CSRF protection answers: "Did this form submission really come from our website?"
- Password hashing answers: "If the database is leaked, are raw passwords exposed?"
- Permissions answer: "Can this user read, create, update, or delete this resource?"
- Middleware answers: "What security checks happen around every request?"

This project mainly uses server-side Django security, not stateless JWT security.

---

## 1. What Security Type This Project Uses

This project uses traditional Django web application security.

That means users log in through a normal HTML login form. Django checks the username and password. If the credentials are correct, Django marks the browser as authenticated. After that, protected pages can check `request.user` and decide whether to allow access.

The project also exposes API routes through Django REST Framework. Those API routes use DRF authentication and permission classes. By default, the API requires an authenticated user.

Configured in:

- `studentsystem/studentsystem/settings.py`
- `studentsystem/accounts/views.py`
- `studentsystem/accounts/forms.py`
- `studentsystem/accounts/models.py`
- `studentsystem/api/views.py`
- `studentsystem/api/urls.py`
- `studentsystem/templates/*/*.html`

---

## 2. What This Project Does Not Use

This project does not use JWT tokens.

There is no package such as:

- `djangorestframework-simplejwt`
- `PyJWT`
- `rest_framework.authtoken`

There is no JWT configuration like:

```python
SIMPLE_JWT = {...}
```

There is no API token authentication like:

```python
TokenAuthentication
```

There is no code that creates access tokens or refresh tokens.

So if someone asks, "Where are JWT tokens generated?", the answer is:

They are not generated in this project.

If someone asks, "Where is token refresh handled?", the answer is:

There is no token refresh system because the project is not using JWT access/refresh tokens.

If someone asks, "Where is bearer token authentication configured?", the answer is:

It is not configured.

---

## 3. Important Clarification About Sessions

You said the project does not use session tokens. That is true if we mean custom session tokens or manually created token-based authentication.

But technically, Django's normal login system uses Django's built-in session framework behind the scenes.

In this project, the settings include:

```python
'django.contrib.sessions'
```

and middleware includes:

```python
'django.contrib.sessions.middleware.SessionMiddleware'
```

Configured in:

- `studentsystem/studentsystem/settings.py`

Also, the login view calls:

```python
login(request, user)
```

Configured in:

- `studentsystem/accounts/views.py`

That means when a user logs in from the browser, Django stores login state using its session system. The browser receives a session cookie, and Django uses that cookie to recognize the same user on later requests.

This is not the same as JWT authentication.

In JWT authentication, the client usually sends an `Authorization: Bearer <token>` header. The server reads the token itself and verifies it. In this project, that is not happening.

In this project, browser login is based on Django's classic server-side session authentication.

Simple comparison:

| Feature                   | JWT Auth                  | This Project |
|---|---|---|
| Access token              | No                            | No |
| Refresh token             | No                            | No |
| Bearer token header       | No                            | No |
| Django login form         | Usually no                    | Yes |
| Django session cookie     | Usually no                    | Yes |
| `request.user`            | Yes, after auth               | Yes |
| Server-side login state   | Usually stateless             | Yes |

So the accurate statement is:

This project does not use JWT tokens or custom API tokens. It uses Django's built-in username/password authentication with server-side session-backed login for browser users.

---

## 4. Authentication: How the Project Knows Who the User Is

Authentication means proving identity.

In this project, authentication is handled by Django's built-in authentication system.

The user enters username and password in the login form. Django validates those credentials using `AuthenticationForm`. If they are correct, the view calls Django's `login()` function.

Configured in:

- `studentsystem/accounts/forms.py`
- `studentsystem/accounts/views.py`
- `studentsystem/templates/accounts/login.html`

The login form is:

```python
class LoginForm(AuthenticationForm):
```

This is important. The project is not manually checking passwords like this:

```python
if password == user.password:
```

That would be insecure because Django passwords are hashed, not stored as plain text.

Instead, `AuthenticationForm` uses Django's authentication backend. It checks the submitted password safely against the stored password hash.

The login view is:

```python
def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('accounts:dashboard')
```

This means:

1. The form receives login data.
2. Django validates the username and password.
3. `form.get_user()` returns the authenticated user.
4. `login(request, user)` marks the user as logged in.
5. The user is redirected to the dashboard.

Logout is handled using:

```python
logout(request)
```

Configured in:

- `studentsystem/accounts/views.py`

Logout removes the authenticated state from the user's browser session.

---

## 5. Custom User Model

This project uses a custom user model instead of Django's default `User` model.

Configured in:

- `studentsystem/accounts/models.py`
- `studentsystem/studentsystem/settings.py`

The custom user model is:

```python
class User(AbstractUser):
```

and the settings file declares:

```python
AUTH_USER_MODEL = 'accounts.User'
```

This is a major security and design decision.

Django's `AbstractUser` already gives the project:

- username
- password hashing support
- login support
- permissions support
- `is_active`
- `is_staff`
- `is_superuser`
- last login tracking
- date joined

This project extends that user with:

- `email`
- `role`
- `phone_number`
- `profile_picture`
- `is_verified`
- `created_at`
- `updated_at`

The most security-relevant custom field is:

```python
role = models.CharField(...)
```

The role decides what type of user this is.

Available roles:

- `SUPER_ADMIN`
- `ADMIN`
- `FACULTY`
- `STUDENT`
- `PARENT`

The model also defines:

```python
def is_admin_role(self):
    return self.role in [self.Roles.ADMIN, self.Roles.SUPER_ADMIN] or self.is_superuser
```

This method is used throughout the project to decide whether a user should have admin-level access.

The important idea:

Authentication says, "This is Kiran."

Authorization says, "Kiran is an admin, so Kiran can manage users."

The role field is the foundation of authorization in this project.

---

## 6. Password Security

This project uses Django's password system through:

- `UserCreationForm`
- `AuthenticationForm`
- `AbstractUser`
- `set_password()`
- Django password validators

Configured in:

- `studentsystem/accounts/forms.py`
- `studentsystem/api/serializers.py`
- `studentsystem/studentsystem/settings.py`

The settings file contains:

```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

These validators protect against weak passwords.

They check things like:

- Is the password too similar to the username or email?
- Is the password too short?
- Is the password too common?
- Is the password only numbers?

The project's forms use `UserCreationForm`, which means password creation is handled by Django's standard secure mechanism.

Configured in:

- `RegistrationForm`
- `StudentCreateForm`
- `UserOnboardingForm`

These classes are in:

- `studentsystem/accounts/forms.py`

In the API serializer, password storage is also handled properly:

```python
user.set_password(password)
```

Configured in:

- `studentsystem/api/serializers.py`

This is very important. `set_password()` does not save the raw password. It hashes the password before saving it.

Bad insecure approach:

```python
user.password = password
```

Good secure approach used here:

```python
user.set_password(password)
```

Why does this matter?

If raw passwords are stored and the database is leaked, every user's password is immediately exposed.

If hashed passwords are stored, attackers cannot directly read the original passwords. They would have to attempt expensive password cracking.

Django also includes modern password hashing algorithms and upgrade behavior.

So the password security model is:

1. Passwords are accepted through Django forms or serializers.
2. Passwords are validated by Django validators.
3. Passwords are hashed before being stored.
4. Login checks the submitted password against the hash.

---

## 7. Page Protection With `login_required`

Many views in the project are protected with:

```python
@login_required
```

Configured in:

- `studentsystem/accounts/views.py`
- `studentsystem/learning/views.py`
- `studentsystem/chatbot/views.py`
- `studentsystem/faculty/views.py`
- `studentsystem/student/views.py`
- `studentsystem/parents/views.py`
- `studentsystem/attendence/views.py`
- `studentsystem/notifications/views.py`
- `studentsystem/placements/views.py`
- `studentsystem/admissions/views.py`
- `studentsystem/results/views.py`

`login_required` is a Django decorator.

It says:

If the user is logged in, allow the view to run.

If the user is not logged in, redirect the user to the login page.

The login URL is configured in:

```python
LOGIN_URL = 'accounts:login'
```

Configured in:

- `studentsystem/studentsystem/settings.py`

For example:

```python
@login_required
def dashboard_redirect(request):
```

This means a random unauthenticated visitor cannot directly open the dashboard route.

Security lesson:

Every page that shows private student, faculty, assignment, result, attendance, notification, or profile data should be protected by `login_required`.

This project follows that pattern in many places.

---

## 8. Authorization: Admin Users vs Normal Users

Authentication alone is not enough.

Suppose a student logs in. The student is authenticated. But should the student be allowed to delete another student account? No.

That is where authorization is needed.

This project uses role-based authorization.

The central role check is:

```python
request.user.is_admin_role()
```

Configured in:

- `studentsystem/accounts/models.py`

Admin-only views use custom decorators such as:

```python
def admin_required(view_func):
```

Configured in:

- `studentsystem/accounts/views.py`
- `studentsystem/learning/views.py`

In `accounts/views.py`, the decorator does:

```python
if not request.user.is_admin_role():
    messages.error(request, 'Admin access is required.')
    return redirect('accounts:student_dashboard')
```

In plain language:

If you are not an admin, you are not allowed to use this admin view.

Admin-protected examples include:

- student list
- user list
- user create
- user update
- user delete
- student create
- student update
- student delete

Configured in:

- `studentsystem/accounts/views.py`

Learning management admin actions are also protected:

- subject create
- subject update
- subject delete
- material upload
- material update
- material delete
- assignment create
- assignment update
- assignment delete

Configured in:

- `studentsystem/learning/views.py`

This is the project's main authorization model:

Logged-in users can view many student system pages, but admin-level users are required for management actions.

---

## 9. Role-Based Decorator Utility

The project also contains a reusable role decorator:

```python
def role_required(*roles):
```

Configured in:

- `studentsystem/accounts/decorators.py`

It works like this:

```python
if request.user.role not in roles:
    raise PermissionDenied
```

This decorator first requires login, then checks whether the user's role is one of the allowed roles.

If the role is not allowed, Django raises `PermissionDenied`, which normally results in a 403 Forbidden response.

The idea is academically important:

Do not simply hide buttons in HTML and call that "security."

Real security must be checked on the server.

This decorator is a server-side authorization check.

Even if a user manually types a URL, the decorator can stop access.

---

## 10. Dashboard Security

The dashboard redirect is protected:

```python
@login_required
def dashboard_redirect(request):
```

Configured in:

- `studentsystem/accounts/views.py`

It sends users to different dashboards depending on role:

```python
if request.user.is_admin_role():
    return redirect('accounts:admin_dashboard')
if request.user.role == User.Roles.STUDENT:
    return redirect('accounts:student_dashboard')
```

This gives role-aware navigation.

Admin dashboard:

```python
@login_required
def admin_dashboard(request):
    if not request.user.is_admin_role():
        return redirect('accounts:student_dashboard')
```

This is good because the view does not merely depend on the user interface. It checks the role again inside the view.

Student dashboard:

```python
@login_required
def student_dashboard(request):
```

This requires login but does not require admin role.

Security lesson:

Dashboards are not just pages. They are entry points into sensitive information. They must always check identity and permissions.

---

## 11. CSRF Protection

CSRF means Cross-Site Request Forgery.

Imagine a user is logged into this student system. Then the user visits a malicious website in another browser tab. That malicious website tries to secretly submit a form to this project, maybe to delete a student or change data.

CSRF protection prevents that.

This project enables CSRF middleware:

```python
'django.middleware.csrf.CsrfViewMiddleware'
```

Configured in:

- `studentsystem/studentsystem/settings.py`

Forms include:

```django
{% csrf_token %}
```

Examples:

- `studentsystem/templates/accounts/login.html`
- `studentsystem/templates/accounts/student_edit.html`
- `studentsystem/templates/accounts/student_form.html`
- `studentsystem/templates/accounts/user_form.html`
- `studentsystem/templates/chatbot/chat.html`
- `studentsystem/templates/learning/form.html`
- `studentsystem/templates/confirm_delete.html`

This is why the project's POST forms are safer.

When Django renders a form, it includes a secret CSRF value. When the form is submitted, Django checks whether the submitted value is valid. If it is missing or wrong, Django rejects the request.

Important lesson:

Login protects who the user is. CSRF protects whether the request genuinely came from your own site.

Both are necessary.

---

## 12. API Security With Django REST Framework

This project uses Django REST Framework.

Configured in:

- `studentsystem/studentsystem/settings.py`
- `studentsystem/api/views.py`
- `studentsystem/api/urls.py`

Installed app:

```python
'rest_framework'
```

The API routes are included at:

```python
path('api/', include('api.urls'))
```

Configured in:

- `studentsystem/studentsystem/urls.py`

The API router exposes endpoints such as:

- `/api/users/`
- `/api/student-profiles/`
- `/api/subjects/`
- `/api/materials/`
- `/api/assignments/`
- `/api/submissions/`
- `/api/chat-messages/`
- `/api/attendance/`
- `/api/results/`
- `/api/notifications/`
- `/api/placement-opportunities/`
- `/api/placement-applications/`
- `/api/admissions/`
- `/api/faculty-profiles/`
- `/api/parent-profiles/`

Configured in:

- `studentsystem/api/urls.py`

The global DRF configuration is:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

Configured in:

- `studentsystem/studentsystem/settings.py`

This means:

1. By default, API users must be authenticated.
2. DRF can authenticate browser users through Django session authentication.
3. DRF can also authenticate requests through HTTP Basic Authentication.
4. JWT authentication is not configured.

Important:

`BasicAuthentication` means the username and password can be sent with the request using the HTTP Basic scheme. This is acceptable only over HTTPS in real production systems. Over plain HTTP, credentials could be exposed.

For development, this is common.

For production, HTTPS is mandatory if Basic Authentication remains enabled.

---

## 13. API Permission Classes

The API does not simply expose everything to everyone.

It defines custom permission classes:

Configured in:

- `studentsystem/api/views.py`

### `AdminWritePermission`

```python
class AdminWritePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.is_admin_role()
```

This means:

- GET, HEAD, and OPTIONS are allowed for authenticated users.
- POST, PUT, PATCH, and DELETE are allowed only for admin users.

This is a good educational example of read/write separation.

Students or normal authenticated users may read certain resources, but only admins can modify them.

Used by:

- student profiles
- subjects
- study materials
- assignments
- attendance records
- results
- notifications
- placement opportunities
- placement applications
- admissions
- faculty profiles
- parent profiles

### `AdminOnlyPermission`

```python
class AdminOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin_role()
```

This means:

The user must be logged in and must be an admin.

Used by:

- `UserViewSet`

This is sensible because user management is highly sensitive.

Creating users, editing users, and deleting users should not be open to ordinary students.

### `IsAuthenticated`

Some viewsets use:

```python
permission_classes = [permissions.IsAuthenticated]
```

Used by:

- `AssignmentSubmissionViewSet`
- `ChatMessageViewSet`

This means the user must be logged in.

The viewsets then further restrict data in `get_queryset()`.

---

## 14. Object-Level Data Protection in API Querysets

A very important security concept is object-level access.

It is not enough to say, "The user is logged in."

You must also ask, "Which records should this user see?"

This project applies that idea in some API viewsets.

### Assignment submissions

Configured in:

- `studentsystem/api/views.py`

```python
def get_queryset(self):
    queryset = AssignmentSubmission.objects.select_related('assignment', 'student')
    if self.request.user.is_admin_role():
        return queryset
    return queryset.filter(student=self.request.user)
```

Meaning:

- Admins can see all submissions.
- Students can see only their own submissions.

When a student creates a submission:

```python
serializer.save(student=self.request.user)
```

Meaning:

The API does not trust the client to choose the student. The server assigns the logged-in user as the submission owner.

This is a strong pattern.

### Chat messages

Configured in:

- `studentsystem/api/views.py`

```python
def get_queryset(self):
    if self.request.user.is_admin_role():
        return ChatMessage.objects.all()
    return ChatMessage.objects.filter(user=self.request.user)
```

Meaning:

- Admins can see all chat messages.
- Normal users can see only their own chat messages.

When a message is created:

```python
serializer.save(user=self.request.user, answer=build_study_answer(question))
```

Again, the server assigns ownership.

Security lesson:

Never trust the browser or API client to honestly say, "This record belongs to me." The server should decide ownership from `request.user`.

---

## 15. Public API Endpoint

The health endpoint is public:

```python
@permission_classes([permissions.AllowAny])
def health(request):
    return Response({'status': 'ok'})
```

Configured in:

- `studentsystem/api/views.py`

Route:

```python
path('health/', views.health, name='api_health')
```

Configured in:

- `studentsystem/api/urls.py`

This endpoint is intentionally open. It does not expose private student data. It only says:

```json
{"status": "ok"}
```

That is common for health checks.

---

## 16. Protection Against SQL Injection

The project uses Django ORM queries such as:

```python
User.objects.filter(...)
get_object_or_404(...)
AssignmentSubmission.objects.filter(...)
```

Configured across:

- `studentsystem/accounts/views.py`
- `studentsystem/learning/views.py`
- `studentsystem/api/views.py`

Django ORM automatically parameterizes database queries. That greatly reduces SQL injection risk compared with manually building SQL strings.

Bad insecure style:

```python
sql = "SELECT * FROM users WHERE username = '" + username + "'"
```

Good style used in this project:

```python
User.objects.filter(username=username)
```

Security lesson:

The ORM acts like a safe translator between Python objects and SQL queries.

This project generally uses ORM methods instead of raw SQL, which is good.

---

## 17. Protection Through Forms and ModelForms

This project uses Django forms and model forms.

Configured in:

- `studentsystem/accounts/forms.py`
- `studentsystem/learning/forms.py`

Forms help security because they:

- validate input
- convert input into expected Python types
- restrict which model fields can be edited
- render fields consistently
- integrate with CSRF-protected templates

For example, `UserProfileUpdateForm` removes the password field:

```python
password = None
```

Configured in:

- `studentsystem/accounts/forms.py`

That prevents the normal profile edit form from displaying or editing the password hash directly.

Another example:

```python
class StudentCreateForm(UserCreationForm):
```

This form uses Django's built-in password creation behavior.

Security lesson:

Forms are not just for HTML convenience. They are part of the input validation boundary.

---

## 18. File Upload Security

The project accepts uploaded files for:

- profile pictures
- study materials
- assignments
- assignment submissions

Configured in models such as:

- `studentsystem/accounts/models.py`
- `studentsystem/learning/models.py`

Media settings:

```python
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

Configured in:

- `studentsystem/studentsystem/settings.py`

During development, media files are served with:

```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Configured in:

- `studentsystem/studentsystem/urls.py`

This is acceptable for local development.

However, file upload security is an area where a real production system needs extra care.

Current protections:

- Django stores uploaded files in controlled upload folders.
- Forms decide which fields accept files.
- Only authenticated/admin users can reach many upload forms.

Production recommendations:

- Validate file types.
- Validate file sizes.
- Store files outside the code directory.
- Use a production media server or cloud storage.
- Do not execute uploaded files.
- Restrict private media access when needed.

Example risk:

If anyone can upload any file type and the server later serves it carelessly, an attacker might upload harmful content.

In this project, upload access is limited by login/admin checks in many flows, but file validation can still be improved.

---

## 19. Clickjacking Protection

The project includes:

```python
'django.middleware.clickjacking.XFrameOptionsMiddleware'
```

Configured in:

- `studentsystem/studentsystem/settings.py`

Clickjacking is when an attacker embeds your site in an invisible frame and tricks users into clicking buttons they did not intend to click.

Django's clickjacking middleware sends a response header that tells browsers not to allow the site to be framed in unsafe ways.

Security lesson:

Some attacks do not steal passwords directly. They trick already logged-in users into performing actions. Clickjacking protection reduces that risk.

---

## 20. General Security Middleware

The project includes:

```python
'django.middleware.security.SecurityMiddleware'
```

Configured in:

- `studentsystem/studentsystem/settings.py`

This middleware provides a place for several Django security features, especially in production.

Examples of settings commonly used with it:

- `SECURE_SSL_REDIRECT`
- `SECURE_HSTS_SECONDS`
- `SECURE_CONTENT_TYPE_NOSNIFF`
- `SECURE_REFERRER_POLICY`

This project currently does not configure many production security headers explicitly.

That is normal for a learning/development project, but production deployment should harden these settings.

---

## 21. Message Framework

The project uses Django messages:

```python
messages.success(...)
messages.error(...)
```

Configured in:

- `studentsystem/accounts/views.py`
- `studentsystem/learning/views.py`

The middleware includes:

```python
'django.contrib.messages.middleware.MessageMiddleware'
```

Configured in:

- `studentsystem/studentsystem/settings.py`

Messages are not authentication by themselves. But they are useful for secure user experience.

For example, when a non-admin tries to access an admin page, the project can show:

```python
messages.error(request, 'Admin access is required.')
```

This gives feedback without exposing sensitive data.

---

## 22. Admin Site Security

The Django admin route is enabled:

```python
path('admin/', admin.site.urls)
```

Configured in:

- `studentsystem/studentsystem/urls.py`

Django admin uses Django's built-in admin authentication and permission system.

Only users with proper staff/admin flags can access it.

Important fields inherited from `AbstractUser`:

- `is_staff`
- `is_superuser`
- `is_active`

The project also has custom roles such as `ADMIN` and `SUPER_ADMIN`, but Django admin itself mainly respects Django's built-in admin flags.

Security lesson:

Application roles and Django admin flags are related but not identical.

A user can have role `ADMIN` in the application, but Django admin access normally also requires `is_staff=True`.

---

## 23. Route-Level Security Map

Main route configuration:

Configured in:

- `studentsystem/studentsystem/urls.py`

Routes:

- `/` goes to the public home page.
- `/admin/` goes to Django admin.
- `/accounts/` contains login, dashboard, users, and student management.
- `/learning/` contains subjects, materials, and assignments.
- `/chatbot/` contains the chatbot interface.
- `/student/`, `/faculty/`, `/parents/`, `/attendence/`, `/notifications/`, `/placements/`, `/admissions/`, `/results/` contain module-specific pages.
- `/api/` contains REST API endpoints.

Security is not mainly configured in the URL file itself. The URL file connects paths to views. The views and DRF viewsets enforce login and permissions.

Security lesson:

URL routing says, "Where does this request go?"

View decorators and permission classes say, "Is this request allowed?"

---

## 24. API Authentication Classes Actually Configured

The project configures:

```python
SessionAuthentication
BasicAuthentication
```

Configured in:

- `studentsystem/studentsystem/settings.py`

### SessionAuthentication

This lets API requests from a logged-in browser user use the same Django session login.

Example:

1. User logs into the website.
2. Browser stores Django session cookie.
3. Browser opens `/api/subjects/`.
4. DRF sees the session-authenticated user.
5. Permissions are checked.

### BasicAuthentication

This allows API clients to send username and password using HTTP Basic Authentication.

Example header:

```http
Authorization: Basic base64(username:password)
```

This is not JWT.

This is not token authentication.

This sends credentials with the request, so it should only be used over HTTPS in production.

---

## 25. How a Normal Login Request Flows

Let us trace the login process like a professor drawing it on a board.

1. User visits `/accounts/login/`.
2. Django renders `studentsystem/templates/accounts/login.html`.
3. The form includes `{% csrf_token %}`.
4. User enters username and password.
5. Browser submits a POST request.
6. `CsrfViewMiddleware` checks the CSRF token.
7. `LoginForm(AuthenticationForm)` validates credentials.
8. If valid, `login(request, user)` logs the user in.
9. Django session middleware stores login state.
10. User is redirected to the dashboard.
11. Later views use `request.user` to know who is logged in.

Configured across:

- `studentsystem/templates/accounts/login.html`
- `studentsystem/accounts/forms.py`
- `studentsystem/accounts/views.py`
- `studentsystem/studentsystem/settings.py`

---

## 26. How an Admin-Only Page Request Flows

Example: admin opens student list.

1. User requests the student list URL.
2. URL routes the request to the view.
3. The view has `@admin_required`.
4. `admin_required` first requires login.
5. If user is not logged in, Django redirects to login.
6. If user is logged in, the decorator checks `request.user.is_admin_role()`.
7. If user is admin, the view runs.
8. If user is not admin, the user is redirected away with an error message.

Configured in:

- `studentsystem/accounts/views.py`
- `studentsystem/accounts/models.py`

Security lesson:

This is server-side access control. It does not depend on hiding links in the frontend.

---

## 27. How an API Request Flows

Example: a logged-in user requests `/api/subjects/`.

1. Request enters Django.
2. URL routes `/api/` to API routes.
3. DRF router sends request to `SubjectViewSet`.
4. DRF authenticates the request using session or basic authentication.
5. DRF checks permissions.
6. `AdminWritePermission` allows safe read methods for authenticated users.
7. If method is GET and user is authenticated, data is returned.
8. If method is POST and user is not admin, request is denied.
9. If method is POST and user is admin, creation is allowed.

Configured in:

- `studentsystem/studentsystem/settings.py`
- `studentsystem/api/urls.py`
- `studentsystem/api/views.py`

---

## 28. Current Development Security Limitations

This project is currently configured like a development project.

The settings include:

```python
DEBUG = True
ALLOWED_HOSTS = []
```

Configured in:

- `studentsystem/studentsystem/settings.py`

This is fine for local development, but not for production.

Production risks:

- `DEBUG=True` can expose detailed error pages.
- Empty `ALLOWED_HOSTS` is not correct for deployment.
- The secret key is directly written in the settings file.
- No HTTPS-only cookie settings are configured.
- No HSTS settings are configured.
- The Gemini API key has a hardcoded fallback value.
- SQLite is used as the database.
- Uploaded media is served directly by Django in debug mode.

These are not unusual in a workshop project, but they should be fixed before production.

Recommended production changes:

```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

Also move API keys fully into environment variables.

---

## 29. Secret Key and External API Key

The project contains:

```python
SECRET_KEY = 'django-insecure-...'
```

Configured in:

- `studentsystem/studentsystem/settings.py`

The Django secret key is used for cryptographic signing.

It helps protect:

- signed cookies
- password reset tokens
- CSRF-related signing behavior
- other cryptographic operations in Django

In production, the secret key must not be committed to source code.

The project also contains:

```python
GEMINI_API_KEY = os.environ.get(
    'GEMINI_API_KEY',
    '...hardcoded fallback...',
)
```

Configured in:

- `studentsystem/studentsystem/settings.py`

This means the project first checks the environment variable, but if it is missing, it uses the hardcoded fallback key.

For a real deployed project, remove the hardcoded fallback and require the key from the environment.

Better production pattern:

```python
GEMINI_API_KEY = os.environ['GEMINI_API_KEY']
```

Security lesson:

Secrets should live in the deployment environment, not inside the code.

---

## 30. Database Security

The project uses SQLite:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Configured in:

- `studentsystem/studentsystem/settings.py`

SQLite is excellent for learning and local development.

For production, a server database such as PostgreSQL is usually preferred.

Security considerations:

- Protect the database file from direct download.
- Do not place `db.sqlite3` in a public static/media directory.
- Do not commit real production databases.
- Use proper file permissions.
- Use backups.

The project's database is inside the project directory, which is common for local Django development.

---

## 31. What Happens When a User Is Deleted

The project uses `get_object_or_404()` before delete operations.

Example:

```python
user = get_object_or_404(User, pk=pk)
```

Configured in:

- `studentsystem/accounts/views.py`

Delete operations usually require POST:

```python
if request.method == 'POST':
    user.delete()
```

This is good because delete actions should not happen through simple GET requests.

The confirmation form includes:

```django
{% csrf_token %}
```

Configured in:

- `studentsystem/templates/confirm_delete.html`

Security lesson:

Dangerous actions like delete should require:

1. authentication
2. authorization
3. POST method
4. CSRF token
5. confirmation UI

This project follows that pattern for many delete flows.

---

## 32. What Security Is Used in One Sentence

This project uses Django's built-in username/password authentication, Django session-backed browser login, role-based authorization, `login_required` decorators, custom admin checks, DRF session/basic authentication, DRF permission classes, CSRF protection, password hashing and validation, ORM-based database access, and basic middleware security.

It does not use JWT access tokens, JWT refresh tokens, bearer token authentication, or custom API tokens.

---

## 33. Security Configuration Location Summary

| Security Feature | Where Configured |
|---|---|
| Custom user model | `studentsystem/accounts/models.py` |
| `AUTH_USER_MODEL` | `studentsystem/studentsystem/settings.py` |
| Login form | `studentsystem/accounts/forms.py` |
| Login/logout views | `studentsystem/accounts/views.py` |
| Password validators | `studentsystem/studentsystem/settings.py` |
| Login redirect settings | `studentsystem/studentsystem/settings.py` |
| Session middleware | `studentsystem/studentsystem/settings.py` |
| CSRF middleware | `studentsystem/studentsystem/settings.py` |
| CSRF tokens in forms | `studentsystem/templates/*/*.html` |
| Page login protection | `@login_required` in app views |
| Admin role check | `is_admin_role()` in `studentsystem/accounts/models.py` |
| Admin-only decorators | `studentsystem/accounts/views.py`, `studentsystem/learning/views.py` |
| Role decorator | `studentsystem/accounts/decorators.py` |
| DRF authentication | `REST_FRAMEWORK` in `studentsystem/studentsystem/settings.py` |
| DRF permissions | `studentsystem/api/views.py` |
| API routing | `studentsystem/api/urls.py` |
| Project routing | `studentsystem/studentsystem/urls.py` |
| Media upload paths | model `FileField` and `ImageField` definitions |
| Media settings | `studentsystem/studentsystem/settings.py` |
| Clickjacking protection | `XFrameOptionsMiddleware` in `studentsystem/studentsystem/settings.py` |
| General security middleware | `SecurityMiddleware` in `studentsystem/studentsystem/settings.py` |

---

## 34. Final Professor-Style Explanation

If I were explaining this to a beginner in a university lecture, I would say:

This project is a classic Django security design. It does not ask every request to carry a JWT. Instead, it lets Django handle login in the traditional server-side way. The student or admin enters a username and password, Django validates the password safely, and Django remembers that login using its session framework.

After login, every important page asks, "Is there a logged-in user?" That is done with `login_required`. For more powerful actions, such as creating users or deleting students, the project asks a second question: "Is this user an admin?" That is done using the custom role field and `is_admin_role()`.

For API routes, the project uses Django REST Framework. The API also requires authentication by default, and custom permission classes decide whether the user can only read data or also write data. Admins can perform management operations; normal authenticated users are more restricted.

For forms, the project uses CSRF protection. That prevents a malicious website from silently submitting dangerous forms on behalf of a logged-in user. For passwords, the project uses Django's hashing and validation system, meaning raw passwords are not stored directly.

Therefore, the security of this project is not token-based security. It is Django framework security: authentication, sessions, decorators, roles, permissions, CSRF, password hashing, and ORM safety working together.

That is the correct way to describe it.
