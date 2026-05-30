# Project Tree Diagram

Excluded from this diagram:

- `guide/`
- `venv/`
- Markdown note files
- `.git/`
- `__pycache__/`
- compiled Python files such as `.pyc`

```text
django_workshop/
|-- .gitignore
|-- studentsystem.rar
`-- studentsystem/
    |-- db.sqlite3
    |-- manage.py
    |-- requirements.txt
    |-- accounts/
    |   |-- __init__.py
    |   |-- admin.py
    |   |-- apps.py
    |   |-- decorators.py
    |   |-- forms.py
    |   |-- models.py
    |   |-- tests.py
    |   |-- urls.py
    |   |-- views.py
    |   `-- migrations/
    |       |-- __init__.py
    |       `-- 0001_initial.py
    |-- admissions/
    |   |-- __init__.py
    |   |-- admin.py
    |   |-- apps.py
    |   |-- models.py
    |   |-- tests.py
    |   |-- urls.py
    |   |-- views.py
    |   `-- migrations/
    |       |-- __init__.py
    |       `-- 0001_initial.py
    |-- api/
    |   |-- __init__.py
    |   |-- serializers.py
    |   |-- urls.py
    |   `-- views.py
    |-- assignments/
    |   |-- __init__.py
    |   |-- admin.py
    |   |-- apps.py
    |   |-- models.py
    |   |-- tests.py
    |   |-- urls.py
    |   |-- views.py
    |   `-- migrations/
    |       `-- __init__.py
    |-- attendence/
    |   |-- __init__.py
    |   |-- admin.py
    |   |-- apps.py
    |   |-- models.py
    |   |-- tests.py
    |   |-- urls.py
    |   |-- views.py
    |   `-- migrations/
    |       |-- __init__.py
    |       `-- 0001_initial.py
    |-- chatbot/
    |   |-- __init__.py
    |   |-- admin.py
    |   |-- apps.py
    |   |-- models.py
    |   |-- tests.py
    |   |-- urls.py
    |   |-- views.py
    |   `-- migrations/
    |       |-- __init__.py
    |       `-- 0001_initial.py
    |-- faculty/
    |   |-- __init__.py
    |   |-- admin.py
    |   |-- apps.py
    |   |-- models.py
    |   |-- tests.py
    |   |-- urls.py
    |   |-- views.py
    |   `-- migrations/
    |       |-- __init__.py
    |       `-- 0001_initial.py
    |-- learning/
    |   |-- __init__.py
    |   |-- admin.py
    |   |-- apps.py
    |   |-- forms.py
    |   |-- models.py
    |   |-- tests.py
    |   |-- urls.py
    |   |-- views.py
    |   `-- migrations/
    |       |-- __init__.py
    |       `-- 0001_initial.py
    |-- media/
    |   |-- profiles/
    |   |   |-- pngwing.com_48.png
    |   |   |-- pngwing.com_51.png
    |   |   `-- pngwing.com_78.png
    |   `-- study_materials/
    |       `-- introduction_to_datascience_book_1.pdf
    |-- notifications/
    |   |-- __init__.py
    |   |-- admin.py
    |   |-- apps.py
    |   |-- models.py
    |   |-- tests.py
    |   |-- urls.py
    |   |-- views.py
    |   `-- migrations/
    |       |-- __init__.py
    |       `-- 0001_initial.py
    |-- parents/
    |   |-- __init__.py
    |   |-- admin.py
    |   |-- apps.py
    |   |-- models.py
    |   |-- tests.py
    |   |-- urls.py
    |   |-- views.py
    |   `-- migrations/
    |       |-- __init__.py
    |       `-- 0001_initial.py
    |-- placements/
    |   |-- __init__.py
    |   |-- admin.py
    |   |-- apps.py
    |   |-- models.py
    |   |-- tests.py
    |   |-- urls.py
    |   |-- views.py
    |   `-- migrations/
    |       |-- __init__.py
    |       `-- 0001_initial.py
    |-- results/
    |   |-- __init__.py
    |   |-- admin.py
    |   |-- apps.py
    |   |-- models.py
    |   |-- tests.py
    |   |-- urls.py
    |   |-- views.py
    |   `-- migrations/
    |       |-- __init__.py
    |       `-- 0001_initial.py
    |-- static/
    |   |-- css/
    |   |   `-- style.css
    |   `-- js/
    |       `-- main.js
    |-- student/
    |   |-- __init__.py
    |   |-- admin.py
    |   |-- apps.py
    |   |-- models.py
    |   |-- tests.py
    |   |-- urls.py
    |   |-- views.py
    |   `-- migrations/
    |       `-- __init__.py
    |-- studentsystem/
    |   |-- __init__.py
    |   |-- asgi.py
    |   |-- settings.py
    |   |-- urls.py
    |   `-- wsgi.py
    `-- templates/
        |-- confirm_delete.html
        |-- accounts/
        |   |-- admin_dashboard.html
        |   |-- dashboard.html
        |   |-- home.html
        |   |-- login.html
        |   |-- student_dashboard.html
        |   |-- student_edit.html
        |   |-- student_form.html
        |   |-- student_list.html
        |   |-- user_form.html
        |   `-- user_list.html
        |-- chatbot/
        |   `-- chat.html
        |-- includes/
        |   `-- base.html
        |-- learning/
        |   |-- assignment_detail.html
        |   |-- assignment_list.html
        |   |-- form.html
        |   |-- material_list.html
        |   |-- subject_detail.html
        |   `-- subject_list.html
        `-- simple/
            `-- list.html
```

## Quick Structure Notes

`studentsystem/` is the main Django project folder. It contains `manage.py`, the SQLite database, installed apps, templates, static files, uploaded media, and the inner Django configuration package.

The inner `studentsystem/studentsystem/` package contains core project configuration:

- `settings.py` controls installed apps, middleware, database, templates, static/media files, authentication, and DRF settings.
- `urls.py` connects the root URL routes to each Django app.
- `asgi.py` and `wsgi.py` are deployment entry points.

The app folders such as `accounts/`, `learning/`, `chatbot/`, `api/`, `faculty/`, `student/`, `parents/`, `results/`, and others contain the feature modules of the system.

Most Django apps follow this pattern:

- `models.py` defines database tables.
- `views.py` contains page or API logic.
- `urls.py` maps app URLs to views.
- `admin.py` registers models in Django admin.
- `apps.py` stores app configuration.
- `tests.py` is reserved for tests.
- `migrations/` stores database migration history.

The `api/` app is slightly different because it contains DRF API code:

- `serializers.py` converts model objects to and from JSON.
- `views.py` defines API viewsets and permissions.
- `urls.py` registers API endpoints with a DRF router.

The `templates/` folder contains HTML pages grouped by feature. The `static/` folder contains CSS and JavaScript. The `media/` folder contains uploaded files such as profile images and study materials.
