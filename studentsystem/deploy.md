# Deploy Django Student System on Render

This guide explains how to deploy this Django project on Render from GitHub.

Your repository is:

```txt
https://github.com/HublikarKiran/Django
```

Your Django project is inside this subfolder:

```txt
studentsystem
```

So on Render, always set:

```txt
Root Directory: studentsystem
```

## Why These Steps Are Needed

Django runs differently in production than on your laptop.

For Render deployment, you need:

- `gunicorn` to run Django in production.
- `whitenoise` to serve static files like CSS, JavaScript, and images.
- `dj-database-url` to read Render database URLs easily.
- `psycopg2-binary` to connect Django with PostgreSQL.
- Environment variables so secrets are not stored in GitHub.
- A build script so Render can install packages, collect static files, and run migrations automatically.

## Project Structure Expected by Render

Your project should look like this:

```txt
Django/
  studentsystem/
    manage.py
    requirements.txt
    build.sh
    studentsystem/
      settings.py
      urls.py
      wsgi.py
      asgi.py
```

Render must point to the folder that contains `manage.py`.

## Step 1: Add Required Packages

Open or create this file:

```txt
studentsystem/requirements.txt
```

Make sure these packages are included:

```txt
Django
gunicorn
whitenoise[brotli]
dj-database-url
psycopg2-binary
```

If you already have a virtual environment locally, you can install them:

```bash
pip install gunicorn whitenoise[brotli] dj-database-url psycopg2-binary
pip freeze > requirements.txt
```

Run the command from inside the `studentsystem` folder.

## Step 2: Update Django Settings

Open:

```txt
studentsystem/studentsystem/settings.py
```

Add these imports near the top:

```python
import os
import dj_database_url
```

Update `SECRET_KEY` so Render can use an environment variable:

```python
SECRET_KEY = os.environ.get("SECRET_KEY", SECRET_KEY)
```

Update `DEBUG`:

```python
DEBUG = os.environ.get("RENDER") is None
```

Why:

- Locally, `RENDER` does not exist, so `DEBUG=True`.
- On Render, `RENDER` exists automatically, so `DEBUG=False`.

Update `ALLOWED_HOSTS`:

```python
ALLOWED_HOSTS = []

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
```

If you later add a custom domain, add it also:

```python
ALLOWED_HOSTS += ["yourdomain.com", "www.yourdomain.com"]
```

## Step 3: Add WhiteNoise Middleware

In `settings.py`, find `MIDDLEWARE`.

Add WhiteNoise immediately after Django security middleware:

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    ...
]
```

Why:

Render does not automatically serve Django static files. WhiteNoise lets Django serve collected static files in production.

## Step 4: Configure Database

In `settings.py`, replace the existing `DATABASES` setting with:

```python
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}
```

Why:

- Locally, Django uses SQLite.
- On Render, Django uses the `DATABASE_URL` environment variable.
- `dj_database_url` automatically converts the Render PostgreSQL URL into Django database settings.

## Step 5: Configure Static Files

In `settings.py`, make sure static files are configured like this:

```python
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```

Why:

`collectstatic` copies all static files into `staticfiles`. WhiteNoise then serves them efficiently.

## Step 6: Create Build Script

Create this file:

```txt
studentsystem/build.sh
```

Add:

```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

Why:

Render runs this file during deployment. It:

- Installs Python packages.
- Collects static files.
- Applies database migrations.

On Linux or Git Bash, make it executable:

```bash
chmod a+x build.sh
```

On Windows, it is okay if you cannot run `chmod`; Render can still run the script using `bash build.sh`.

## Step 7: Test Locally

From inside the `studentsystem` folder:

```bash
python manage.py check
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py runserver
```

Open:

```txt
http://127.0.0.1:8000/
```

If the app works locally, commit and push:

```bash
git add studentsystem
git commit -m "Prepare Django project for Render deployment"
git push
```

## Step 8: Create PostgreSQL Database on Render

1. Go to Render Dashboard.
2. Click `New`.
3. Select `PostgreSQL`.
4. Give it a name, for example:

```txt
studentsystem-db
```

5. Choose a plan.
6. Create the database.
7. Copy the `Internal Database URL`.

You will use this as `DATABASE_URL`.

## Step 9: Create Web Service on Render

1. Go to Render Dashboard.
2. Click `New`.
3. Select `Web Service`.
4. Connect your GitHub account.
5. Select:

```txt
HublikarKiran/Django
```

6. Configure the service:

```txt
Name: studentsystem
Runtime: Python
Root Directory: studentsystem
Build Command: bash build.sh
Start Command: gunicorn studentsystem.wsgi:application
```

Why this start command:

Your Django project package is named `studentsystem`, and `wsgi.py` contains the production WSGI application.

## Step 10: Add Environment Variables

In the Render web service settings, add:

```txt
DATABASE_URL = your Render internal database URL
SECRET_KEY = a long random secret key
WEB_CONCURRENCY = 4
```

You can generate a Django secret key locally:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Do not put your production secret key directly in GitHub.

## Step 11: Deploy

Click:

```txt
Create Web Service
```

Render will:

1. Clone your GitHub repository.
2. Enter the `studentsystem` root directory.
3. Run `bash build.sh`.
4. Start your app with Gunicorn.
5. Give you a public `.onrender.com` URL.

## Step 12: Create Django Admin User

After deployment succeeds:

1. Open your Render web service.
2. Open `Shell`.
3. Run:

```bash
python manage.py createsuperuser
```

Enter username, email, and password.

Then visit:

```txt
https://your-service-name.onrender.com/admin/
```

## Step 13: Common Errors and Fixes

### Error: DisallowedHost

Cause:

`ALLOWED_HOSTS` does not include your Render hostname.

Fix:

Make sure this exists in `settings.py`:

```python
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
```

### Error: No module named gunicorn

Cause:

`gunicorn` is missing from `requirements.txt`.

Fix:

Add:

```txt
gunicorn
```

Then commit and push again.

### Error: Static files not loading

Cause:

WhiteNoise or `collectstatic` is not configured correctly.

Fix:

Check:

```python
"whitenoise.middleware.WhiteNoiseMiddleware"
STATIC_ROOT = BASE_DIR / "staticfiles"
```

Also check that `build.sh` contains:

```bash
python manage.py collectstatic --no-input
```

### Error: Database connection failed

Cause:

`DATABASE_URL` is missing or incorrect.

Fix:

Use the Render PostgreSQL `Internal Database URL`, not the external URL.

### Error: Application exited early

Cause:

The start command is wrong.

Fix:

Use:

```bash
gunicorn studentsystem.wsgi:application
```

## Final Checklist

Before deployment, confirm:

- `requirements.txt` exists inside `studentsystem`.
- `build.sh` exists inside `studentsystem`.
- `settings.py` uses environment variables.
- `settings.py` has WhiteNoise configured.
- Render root directory is `studentsystem`.
- Render build command is `bash build.sh`.
- Render start command is `gunicorn studentsystem.wsgi:application`.
- Render environment variables include `DATABASE_URL` and `SECRET_KEY`.

## Recommended Render Settings Summary

```txt
Repository: HublikarKiran/Django
Root Directory: studentsystem
Runtime: Python
Build Command: bash build.sh
Start Command: gunicorn studentsystem.wsgi:application
```

Environment variables:

```txt
DATABASE_URL = Render PostgreSQL internal database URL
SECRET_KEY = generated secret key
WEB_CONCURRENCY = 4
```

