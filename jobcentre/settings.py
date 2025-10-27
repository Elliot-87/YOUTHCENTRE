import os
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Allow iframe embedding for same origin
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Or disable completely for development
X_FRAME_OPTIONS = 'ALLOWALL'

# Also add this for modern browsers
SECURE_CROSS_ORIGIN_OPENER_POLICY = None


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "your-secret-key"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'jobs',
    "accounts",
  

    # Tailwind
    "tailwind",
    "theme",  # your Tailwind app
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "jobcentre.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # your project templates folder
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]



WSGI_APPLICATION = "jobcentre.wsgi.application"

# Database (SQLite for minimal setup)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation (default)
AUTH_PASSWORD_VALIDATORS = []

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'

# 👇 Tell Django to also look inside your theme/static directory
STATICFILES_DIRS = [
    BASE_DIR / "theme" / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"  # this is where collectstatic will copy everything


# Tailwind settings
TAILWIND_APP_NAME = "theme"
INTERNAL_IPS = ["127.0.0.1"]

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"