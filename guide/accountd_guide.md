# Accounts App Guide

The accounts app contains the custom `User` model, roles, login, logout, dashboards, admin onboarding, and student profile management.

Run with:

```powershell
python manage.py runserver
```

Important URLs:

- Login: `/accounts/login/`
- Dashboard: `/accounts/dashboard/`
- Admin dashboard: `/accounts/dashboard/admin/`
- Student dashboard: `/accounts/dashboard/student/`
- User list: `/accounts/users/`
- Onboard user: `/accounts/users/create/`
- Student list: `/accounts/students/`
- Create student profile: `/accounts/students/create/`

Only admin/super admin users can create, edit, or delete users.
