# JWT Tokens Notes

## What JWT Means

JWT means JSON Web Token.

A JWT is a signed token that stores claims about a user. APIs can use JWTs for authentication without storing every token in the database.

A JWT usually has three parts:

```text
header.payload.signature
```

## Is JWT Configured In This Project?

No. JWT authentication is not currently configured.

Current dependency file:

```text
studentsystem/requirements.txt
```

Current dependencies include:

```text
djangorestframework==3.17.1
```

But there is no JWT package such as:

```text
djangorestframework-simplejwt
```

Current DRF settings in:

```text
studentsystem/studentsystem/settings.py
```

```python
DEFAULT_AUTHENTICATION_CLASSES = [
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication',
]
```

There is no JWT authentication class configured.

## Access Token vs Refresh Token

JWT systems commonly use two tokens.

Access token:

- short-lived
- sent with API requests
- proves the user is authenticated

Refresh token:

- longer-lived
- used to get a new access token
- should be stored carefully

## How JWT Would Be Added To This Project

Step 1: Install package:

```bash
pip install djangorestframework-simplejwt
```

Step 2: Add it to:

```text
studentsystem/requirements.txt
```

Example:

```text
djangorestframework-simplejwt
```

Step 3: Configure DRF in:

```text
studentsystem/studentsystem/settings.py
```

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

Step 4: Add JWT routes in:

```text
studentsystem/studentsystem/urls.py
```

```python
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    ...
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

## How To Get JWT Tokens

Request:

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"password\"}"
```

Example response:

```json
{
  "refresh": "refresh-token-value",
  "access": "access-token-value"
}
```

## How To Call APIs With JWT

Use the access token:

```bash
curl http://127.0.0.1:8000/api/subjects/ \
  -H "Authorization: Bearer access-token-value"
```

## How To Refresh JWT Access Token

Request:

```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d "{\"refresh\":\"refresh-token-value\"}"
```

Response:

```json
{
  "access": "new-access-token-value"
}
```

## JWT And This Project's Permissions

JWT only authenticates the user.

After authentication, this project's existing permissions still apply:

- `UserViewSet` requires admin access.
- `AdminWritePermission` allows authenticated read but admin-only write.
- `AssignmentSubmissionViewSet` filters non-admin users to their own submissions.
- `ChatMessageViewSet` filters non-admin users to their own messages.

## Token Authentication vs JWT

DRF token authentication:

- token is stored in the database
- usually one token per user
- simple to implement

JWT authentication:

- token is signed
- access token can expire quickly
- refresh token gets new access tokens
- common for modern frontend/mobile apps

## Security Notes

- Always use HTTPS in production.
- Keep refresh tokens secure.
- Use short lifetimes for access tokens.
- Do not store JWTs in public code.
- Do not commit real production secrets into Git.

