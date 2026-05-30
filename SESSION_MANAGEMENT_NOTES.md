# Session Management Notes

## What A Session Is

A session stores information about a user across multiple requests.

HTTP itself is stateless. Without sessions, every request is separate and Django would not remember that a user already logged in.

## Where Sessions Are Configured

Main settings file:

```text
studentsystem/studentsystem/settings.py
```

Installed app:

```python
'django.contrib.sessions'
```

Middleware:

```python
'django.contrib.sessions.middleware.SessionMiddleware'
```

Authentication middleware:

```python
'django.contrib.auth.middleware.AuthenticationMiddleware'
```

Order matters:

- `SessionMiddleware` loads session data.
- `AuthenticationMiddleware` uses the session to set `request.user`.

## Login Creates A Session

Configured in:

```text
studentsystem/accounts/views.py
```

Code:

```python
login(request, user)
```

When this runs:

- Django saves the user ID in the session
- the browser receives a session cookie
- future requests include that cookie
- Django restores `request.user`

## Logout Destroys The Session

Configured in:

```text
studentsystem/accounts/views.py
```

Code:

```python
logout(request)
```

This clears the authenticated user from the session.

## Session Login URL

Configured in:

```text
studentsystem/accounts/urls.py
```

Route:

```text
/accounts/login/
```

Logout route:

```text
/accounts/logout/
```

## Session-Based Page Protection

Views are protected using:

```python
@login_required
```

Example:

```python
@login_required
def dashboard_redirect(request):
    ...
```

If the user is not logged in, Django redirects to:

```python
LOGIN_URL = 'accounts:login'
```

## Sessions And DRF

Configured in:

```text
studentsystem/studentsystem/settings.py
```

DRF authentication:

```python
'rest_framework.authentication.SessionAuthentication'
```

This allows logged-in browser users to access the browsable API using their existing Django session.

Example:

1. User logs in at `/accounts/login/`.
2. User opens `/api/subjects/` in the browser.
3. DRF sees the session cookie.
4. DRF treats the request as authenticated.

## CSRF And Sessions

This project includes:

```python
'django.middleware.csrf.CsrfViewMiddleware'
```

For session-authenticated unsafe requests like `POST`, `PUT`, `PATCH`, and `DELETE`, CSRF protection matters.

In browser forms, templates include:

```django
{% csrf_token %}
```

For API tools like curl/Postman, Basic Auth is often easier than session auth because session auth can require CSRF handling.

## Where Session Data Is Stored

This project does not override Django's default session engine.

By default, Django stores sessions in the database table:

```text
django_session
```

The database is configured in:

```text
studentsystem/studentsystem/settings.py
```

Current database:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

So sessions are stored in:

```text
studentsystem/db.sqlite3
```

## Session Management Summary

Configured pieces:

- `django.contrib.sessions`
- `SessionMiddleware`
- `AuthenticationMiddleware`
- `login(request, user)`
- `logout(request)`
- `@login_required`
- DRF `SessionAuthentication`

Main project files:

```text
studentsystem/studentsystem/settings.py
studentsystem/accounts/views.py
studentsystem/accounts/urls.py
```

