import os

import dj_database_url
from dotenv import load_dotenv

from project import dirs

load_dotenv()

SECRET_KEY = os.getenv("APP_SECRET_KEY") or "1"

DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "*",
]

INSTALLED_APPS = [
    "app_jana_sergienko",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "health_check",
    "health_check.contrib.migrations",
    "health_check.db",
    "silk",
]

MIDDLEWARE = [
    "silk.middleware.SilkyMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            dirs.DIR_PROJECT / "templates" / "project",
        ],
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

WSGI_APPLICATION = "project.wsgi.application"

_db_url = os.getenv("DATABASE_URL")
assert _db_url, "db url is not configured"

DATABASES = {
    "default": dj_database_url.parse(_db_url),
}

_pv = "django.contrib.auth.password_validation"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": f"{_pv}.UserAttributeSimilarityValidator",
    },
    {
        "NAME": f"{_pv}.MinimumLengthValidator",
    },
    {
        "NAME": f"{_pv}.CommonPasswordValidator",
    },
    {
        "NAME": f"{_pv}.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

STATICFILES_DIRS = [
    dirs.DIR_REPO / "project" / "static" / "project",
]

STATIC_ROOT = dirs.DIR_ARTIFACTS / "static"

if not DEBUG:
    STATICFILES_STORAGE = (
        "whitenoise.storage.CompressedManifestStaticFilesStorage"
    )

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SILKY_PYTHON_PROFILER = True


LOGIN_URL = "/auth/login/"
