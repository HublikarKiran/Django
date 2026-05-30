# API App Guide

This package exposes Django REST Framework endpoints.

Base URL:

```text
/api/
```

Health check:

```text
/api/health/
```

Authentication:

- Use Basic Auth in Postman or Thunder Client.
- Username: admin username
- Password: admin password
- For JSON requests, use `Content-Type: application/json`.
- For file upload requests, use `multipart/form-data`.

Common CRUD methods:

- `GET /api/subjects/`
- `POST /api/subjects/`
- `GET /api/subjects/1/`
- `PATCH /api/subjects/1/`
- `PUT /api/subjects/1/`
- `DELETE /api/subjects/1/`

Important endpoint names:

- `users`
- `student-profiles`
- `subjects`
- `materials`
- `assignments`
- `submissions`
- `chat-messages`
- `attendance`
- `results`
- `notifications`
- `placement-opportunities`
- `placement-applications`
- `admissions`
- `faculty-profiles`
- `parent-profiles`

See the main `guide.md` for detailed Postman and Thunder Client examples.
