# Deploy Django Student System on Render Using Docker

This guide explains how to deploy the Django project on Render using a Docker container.

Use this method if you want more control over the runtime environment, Python version, system packages, and deployment behavior.

## Normal Render Deploy vs Docker Deploy

Normal Render Python deploy:

- Render installs Python packages directly.
- You configure build and start commands in the Render dashboard.
- Easier for beginners.

Docker deploy:

- You define the whole app environment in a `Dockerfile`.
- Render builds your Docker image and runs it.
- Better when you want consistent local and production behavior.
- Useful when your app needs OS-level packages or custom setup.

For this project, normal Render deployment is simpler. Docker is useful if you want a professional container-based deployment workflow.

## Project Structure

Your GitHub repository is:

```txt
https://github.com/HublikarKiran/Django
```

Your Django project is inside:

```txt
studentsystem
```

Expected structure:

```txt
Django/
  studentsystem/
    Dockerfile
    .dockerignore
    requirements.txt
    manage.py
    studentsystem/
      settings.py
      urls.py
      wsgi.py
      asgi.py
```

On Render, set:

```txt
Root Directory: studentsystem
```

## Why Use Docker

Docker packages your project with everything it needs to run.

Benefits:

- Same environment locally and on Render.
- Python version is controlled by you.
- Easier to move to another cloud later.
- Dependencies are installed inside the image.
- Production start command is part of the container.

Tradeoffs:

- More files to maintain.
- Slightly more complicated than Render native Python deployment.
- Build errors can take more time to debug.

## Step 1: Add Required Packages

Open:

```txt
studentsystem/requirements.txt
```

Make sure it contains:

```txt
Django
gunicorn
whitenoise[brotli]
dj-database-url
psycopg2-binary
```

Why:

- `Django` is the web framework.
- `gunicorn` runs Django in production.
- `whitenoise` serves static files.
- `dj-database-url` reads the PostgreSQL URL from Render.
- `psycopg2-binary` connects Django to PostgreSQL.

## Step 2: Update Django Settings

Open:

```txt
studentsystem/studentsystem/settings.py
```

Add:

```python
import os
import dj_database_url
```

Use environment variable for secret key:

```python
SECRET_KEY = os.environ.get("SECRET_KEY", SECRET_KEY)
```

Set production debug behavior:

```python
DEBUG = os.environ.get("RENDER") is None
```

Configure allowed hosts:

```python
ALLOWED_HOSTS = []

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
```

Add WhiteNoise middleware after security middleware:

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    ...
]
```

Configure database:

```python
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}
```

Configure static files:

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

## Step 3: Create Dockerfile

Create:

```txt
studentsystem/Dockerfile
```

Add:

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --no-input

EXPOSE 8000

CMD ["gunicorn", "studentsystem.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Why:

- `python:3.12-slim` gives a small Python image.
- `WORKDIR /app` stores the app inside the container.
- `requirements.txt` is copied first so Docker can cache dependency installation.
- `collectstatic` prepares static files during image build.
- `gunicorn` starts Django in production.

## Step 4: Create .dockerignore

Create:

```txt
studentsystem/.dockerignore
```

Add:

```txt
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
db.sqlite3
.git/
.gitignore
.env
staticfiles/
media/
```

Why:

This prevents unnecessary local files from being copied into the Docker image.

Do not copy `.env` into a Docker image because it may contain secrets.

## Step 5: Optional Docker Entrypoint for Migrations

You can run migrations in the container startup command, but it is usually cleaner to run migrations as a Render pre-deploy command or manually from Render Shell.

If you want the container to run migrations every time it starts, create:

```txt
studentsystem/entrypoint.sh
```

Add:

```bash
#!/usr/bin/env bash
set -o errexit

python manage.py migrate
gunicorn studentsystem.wsgi:application --bind 0.0.0.0:${PORT:-8000}
```

Then update the Dockerfile:

```dockerfile
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
```

Why this is optional:

Running migrations during startup is simple, but for larger production projects it can slow startup or cause problems if multiple containers start at once. For a student project or small app, it is usually okay.

## Step 6: Better Render Dockerfile Using PORT

Render provides a `PORT` environment variable for web services.

For better compatibility, use this Dockerfile:

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --no-input

EXPOSE 8000

CMD gunicorn studentsystem.wsgi:application --bind 0.0.0.0:${PORT:-8000}
```

Use this version if Render complains about port binding.

## Step 7: Test Docker Locally

From inside the `studentsystem` folder:

```bash
docker build -t studentsystem .
```

Run with SQLite:

```bash
docker run --rm -p 8000:8000 -e SECRET_KEY=local-test-secret studentsystem
```

Open:

```txt
http://127.0.0.1:8000/
```

If you want to test with a custom port:

```bash
docker run --rm -p 8080:8080 -e PORT=8080 -e SECRET_KEY=local-test-secret studentsystem
```

Open:

```txt
http://127.0.0.1:8080/
```

## Step 8: Run Migrations Locally in Docker

If using SQLite inside the container:

```bash
docker run --rm -e SECRET_KEY=local-test-secret studentsystem python manage.py migrate
```

For real production, migrations should run against PostgreSQL on Render.

## Step 9: Commit and Push

From your repository root:

```bash
git add studentsystem/Dockerfile studentsystem/.dockerignore studentsystem/requirements.txt studentsystem/studentsystem/settings.py
git commit -m "Add Docker deployment setup for Django"
git push
```

If you added `entrypoint.sh`, include it:

```bash
git add studentsystem/entrypoint.sh
git commit -m "Add Docker entrypoint for Django deployment"
git push
```

## Step 10: Create PostgreSQL Database on Render

1. Open Render Dashboard.
2. Click `New`.
3. Select `PostgreSQL`.
4. Name it:

```txt
studentsystem-db
```

5. Create the database.
6. Copy the `Internal Database URL`.

You will add it to the Docker web service as `DATABASE_URL`.

## Step 11: Create Docker Web Service on Render

1. Open Render Dashboard.
2. Click `New`.
3. Select `Web Service`.
4. Connect your GitHub repository:

```txt
HublikarKiran/Django
```

5. Configure:

```txt
Name: studentsystem-docker
Runtime: Docker
Root Directory: studentsystem
Dockerfile Path: ./Dockerfile
```

If Render asks for Docker build context, use:

```txt
.
```

Because the root directory is already `studentsystem`.

## Step 12: Add Environment Variables

Add these in Render:

```txt
DATABASE_URL = Render PostgreSQL internal database URL
SECRET_KEY = generated secret key
WEB_CONCURRENCY = 4
```

Generate a secret key locally:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Do not hard-code this key in `settings.py` or `Dockerfile`.

## Step 13: Run Migrations on Render

If your Docker container does not run migrations automatically, use Render Shell after deployment:

```bash
python manage.py migrate
```

Then create an admin user:

```bash
python manage.py createsuperuser
```

## Step 14: Open the App

After deployment completes, Render gives you a URL like:

```txt
https://studentsystem-docker.onrender.com/
```

Admin panel:

```txt
https://studentsystem-docker.onrender.com/admin/
```

## Step 15: Common Docker Deployment Errors

### Error: No open ports detected

Cause:

Gunicorn is not binding to the port Render expects.

Fix:

Use:

```dockerfile
CMD gunicorn studentsystem.wsgi:application --bind 0.0.0.0:${PORT:-8000}
```

### Error: ModuleNotFoundError

Cause:

The start command points to the wrong Django project name.

Fix:

Use:

```txt
studentsystem.wsgi:application
```

because your Django package is named `studentsystem`.

### Error: Static files missing

Cause:

`collectstatic` did not run or WhiteNoise is not configured.

Fix:

Check Dockerfile:

```dockerfile
RUN python manage.py collectstatic --no-input
```

Check `settings.py`:

```python
"whitenoise.middleware.WhiteNoiseMiddleware"
STATIC_ROOT = BASE_DIR / "staticfiles"
```

### Error: Database connection failed

Cause:

`DATABASE_URL` is missing or wrong.

Fix:

Use the Render PostgreSQL `Internal Database URL`.

### Error: SECRET_KEY missing

Cause:

Render does not have a `SECRET_KEY` environment variable.

Fix:

Add:

```txt
SECRET_KEY = generated secret key
```

in Render environment variables.

## Recommended Docker Setup Summary

Files to add:

```txt
studentsystem/Dockerfile
studentsystem/.dockerignore
```

Render settings:

```txt
Repository: HublikarKiran/Django
Runtime: Docker
Root Directory: studentsystem
Dockerfile Path: ./Dockerfile
```

Environment variables:

```txt
DATABASE_URL = Render PostgreSQL internal database URL
SECRET_KEY = generated secret key
WEB_CONCURRENCY = 4
```

Recommended Docker command inside Dockerfile:

```dockerfile
CMD gunicorn studentsystem.wsgi:application --bind 0.0.0.0:${PORT:-8000}
```

## Which Deployment Should You Choose

Choose normal Render deployment if:

- You are deploying a student project.
- You want the simplest setup.
- You do not need custom system packages.

Choose Docker deployment if:

- You want full control over the environment.
- You want the same setup locally and in production.
- You may deploy the same app to other cloud platforms later.

For this project, start with normal Render deployment first. After it works, Docker deployment is a good next step.

