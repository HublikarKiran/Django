# Student System Guide

This project is a beginner-friendly Django student management system. It uses Django templates, basic HTML, basic CSS, simple JavaScript, SQLite, and Django REST Framework.

No Bootstrap, Tailwind, or external frontend framework is used.

## 1. Project Roles

- Admin and super admin can onboard users.
- Students, faculty, and parents can login only after an admin creates their account.
- Students can view learning content, submit assignments, and use the chatbot.
- Admin can manage users, subjects, materials, assignments, and records.

## 2. Install And Run

Open the terminal in:

```powershell
c:\Users\kiran\Downloads\vignan University\django_workshop
```

Activate the virtual environment:

```powershell
venv\Scripts\activate
```

Go into the Django project:

```powershell
cd studentsystem
```

Install packages:

```powershell
pip install -r requirements.txt
```

Create database tables:

```powershell
python manage.py migrate
```

Create the first admin user:

```powershell
python manage.py createsuperuser
```

Run the server:

```powershell
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Admin panel:

```text
http://127.0.0.1:8000/admin/
```

## 3. Main Pages

- Login: `http://127.0.0.1:8000/accounts/login/`
- Dashboard: `http://127.0.0.1:8000/accounts/dashboard/`
- User onboarding: `http://127.0.0.1:8000/accounts/users/create/`
- Subjects: `http://127.0.0.1:8000/learning/`
- Materials: `http://127.0.0.1:8000/learning/materials/`
- Assignments: `http://127.0.0.1:8000/learning/assignments/`
- Chatbot: `http://127.0.0.1:8000/chatbot/`
- API health check: `http://127.0.0.1:8000/api/health/`

## 4. Admin Onboarding Flow

1. Login as superuser or admin.
2. Open `Accounts > Users` from the navigation.
3. Click `Onboard User`.
4. Enter username, email, name, phone number, role, password, and verification status.
5. Save.
6. Share the username and password with the user.

For students with roll number/course/semester, use:

```text
http://127.0.0.1:8000/accounts/students/create/
```

## 5. API Authentication

The API uses Basic Auth or browser session login.

For Postman or Thunder Client:

- Auth type: `Basic Auth`
- Username: your admin username
- Password: your admin password
- Header for JSON requests: `Content-Type: application/json`

Most create/update/delete requests require an admin user.

## 6. API Endpoints

Base URL:

```text
http://127.0.0.1:8000/api/
```

Health check:

- Method: `GET`
- URL: `http://127.0.0.1:8000/api/health/`
- Auth: not required

List API routes:

- Method: `GET`
- URL: `http://127.0.0.1:8000/api/`
- Auth: Basic Auth

## 7. User API CRUD

List users:

- Method: `GET`
- URL: `http://127.0.0.1:8000/api/users/`

Create user:

- Method: `POST`
- URL: `http://127.0.0.1:8000/api/users/`
- Body type: raw JSON

```json
{
  "username": "student1",
  "password": "Student@12345",
  "email": "student1@example.com",
  "first_name": "Student",
  "last_name": "One",
  "phone_number": "9999999999",
  "role": "STUDENT",
  "is_verified": true,
  "is_active": true
}
```

View one user:

- Method: `GET`
- URL: `http://127.0.0.1:8000/api/users/1/`

Update full user:

- Method: `PUT`
- URL: `http://127.0.0.1:8000/api/users/1/`
- Body type: raw JSON with all required fields.

Update partial user:

- Method: `PATCH`
- URL: `http://127.0.0.1:8000/api/users/1/`

```json
{
  "phone_number": "8888888888",
  "is_verified": true
}
```

Delete user:

- Method: `DELETE`
- URL: `http://127.0.0.1:8000/api/users/1/`

## 8. Subject API CRUD

Create subject:

- Method: `POST`
- URL: `http://127.0.0.1:8000/api/subjects/`
- Body type: raw JSON

```json
{
  "name": "Database Management Systems",
  "code": "DBMS101",
  "description": "Introduction to database concepts."
}
```

List subjects:

- Method: `GET`
- URL: `http://127.0.0.1:8000/api/subjects/`

Update subject:

- Method: `PATCH`
- URL: `http://127.0.0.1:8000/api/subjects/1/`

```json
{
  "description": "Updated DBMS description."
}
```

Delete subject:

- Method: `DELETE`
- URL: `http://127.0.0.1:8000/api/subjects/1/`

## 9. Study Material API

For file upload in Postman or Thunder Client, use `multipart/form-data`.

Create material:

- Method: `POST`
- URL: `http://127.0.0.1:8000/api/materials/`
- Body type: form-data
- Fields:
  - `subject`: subject id, example `1`
  - `title`: material title
  - `description`: notes
  - `file`: choose a PDF/doc/image file

List materials:

- Method: `GET`
- URL: `http://127.0.0.1:8000/api/materials/`

## 10. Assignment API

Create assignment:

- Method: `POST`
- URL: `http://127.0.0.1:8000/api/assignments/`
- Body type: form-data
- Fields:
  - `subject`: `1`
  - `title`: `DBMS Assignment 1`
  - `description`: `Explain normalization`
  - `due_date`: `2026-06-15T10:00:00Z`
  - `file`: optional file

Submit assignment:

- Method: `POST`
- URL: `http://127.0.0.1:8000/api/submissions/`
- Body type: form-data
- Fields:
  - `assignment`: assignment id, example `1`
  - `answer_text`: written answer
  - `file`: answer file

## 11. Chatbot API

Ask a topic:

- Method: `POST`
- URL: `http://127.0.0.1:8000/api/chat-messages/`
- Body type: raw JSON

```json
{
  "question": "Explain DBMS normalization"
}
```

The API creates an answer automatically and saves the chat message.

## 12. Other API Endpoints

- Attendance: `http://127.0.0.1:8000/api/attendance/`
- Results: `http://127.0.0.1:8000/api/results/`
- Notifications: `http://127.0.0.1:8000/api/notifications/`
- Placements: `http://127.0.0.1:8000/api/placement-opportunities/`
- Placement applications: `http://127.0.0.1:8000/api/placement-applications/`
- Admissions: `http://127.0.0.1:8000/api/admissions/`
- Faculty profiles: `http://127.0.0.1:8000/api/faculty-profiles/`
- Parent profiles: `http://127.0.0.1:8000/api/parent-profiles/`

Use the same CRUD methods:

- `GET /endpoint/` list records
- `POST /endpoint/` create record
- `GET /endpoint/id/` view one record
- `PUT /endpoint/id/` replace record
- `PATCH /endpoint/id/` update some fields
- `DELETE /endpoint/id/` delete record

## 13. Thunder Client Steps In VS Code

1. Open Thunder Client extension.
2. Click `New Request`.
3. Enter method and URL.
4. Open `Auth`.
5. Select `Basic Auth`.
6. Enter admin username and password.
7. For JSON, open `Body > JSON` and paste the sample JSON.
8. For file uploads, open `Body > Form` and add text/file fields.
9. Click `Send`.

## 14. Postman Steps

1. Create a new request.
2. Select method: `GET`, `POST`, `PATCH`, `PUT`, or `DELETE`.
3. Enter URL.
4. Open `Authorization`.
5. Select `Basic Auth`.
6. Enter username and password.
7. For JSON, open `Body > raw > JSON`.
8. For file uploads, open `Body > form-data`.
9. Click `Send`.
