# Token Authentication Notes

## What Token Authentication Is

Token authentication lets an API client authenticate by sending a token instead of a browser session cookie or username/password on every request.

Example header:

```text
Authorization: Token abc123
```

## Is Token Authentication Configured In This Project?

No. This project currently does not configure DRF token authentication.

Current DRF authentication in:

```text
studentsystem/studentsystem/settings.py
```

```python
DEFAULT_AUTHENTICATION_CLASSES = [
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication',
]
```

There is no:

```python
'rest_framework.authtoken'
```

in `INSTALLED_APPS`.

There is also no:

```python
'rest_framework.authentication.TokenAuthentication'
```

in `DEFAULT_AUTHENTICATION_CLASSES`.

## Difference Between Session, Basic Auth, And Token Auth

Session authentication:

- best for browser-based web apps
- uses login session cookie
- often needs CSRF for unsafe requests

Basic authentication:

- sends username and password with each request
- useful for testing
- should only be used over HTTPS

Token authentication:

- sends a generated token with each request
- useful for mobile apps, API clients, and integrations
- avoids sending password every time

## How To Add DRF Token Authentication

Step 1: Add app in:

```text
studentsystem/studentsystem/settings.py
```

```python
INSTALLED_APPS = [
    ...
    'rest_framework.authtoken',
]
```

Step 2: Add authentication class:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

Step 3: Run migrations:

```bash
python manage.py migrate
```

Step 4: Add token login endpoint in:

```text
studentsystem/studentsystem/urls.py
```

```python
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    ...
    path('api/token-auth/', obtain_auth_token),
]
```

## How To Get A Token

Request:

```bash
curl -X POST http://127.0.0.1:8000/api/token-auth/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"password\"}"
```

Response:

```json
{
  "token": "generated-token-value"
}
```

## How To Use A Token

Request:

```bash
curl http://127.0.0.1:8000/api/subjects/ \
  -H "Authorization: Token generated-token-value"
```

## Token Authentication And Permissions

Token authentication only identifies the user.

Permissions still decide what the user can do.

In this project:

- `AdminOnlyPermission` still protects user APIs.
- `AdminWritePermission` still allows reads for authenticated users and writes for admins.
- normal users still see only their own chat messages and submissions.

## When To Use Token Authentication

Use token authentication for:

- mobile apps
- API clients
- third-party integrations
- scripts

Do not expose tokens in public frontend JavaScript. Treat tokens like passwords.

