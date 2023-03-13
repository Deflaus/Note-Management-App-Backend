import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-mz7($xilj+$#q6ufewb!do&&l(1h_b7@z$uodwr=8zwsg5s*gc")

DEBUG = bool(int(os.environ.get("DEBUG", 1)))

ALLOWED_HOSTS = list(set(os.environ.get("ALLOWED_HOSTS", "").split("&") + ["localhost", "127.0.0.1"]))

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # DRF
    "rest_framework",
    "rest_framework.authtoken",
    "drf_yasg",
    "corsheaders",
    # Project apps
    "api.apps.ApiConfig",
    "core.apps.CoreConfig",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "note_management_app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "note_management_app.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("SQL_DATABASE", "note_management_app"),
        "USER": os.environ.get("SQL_USER", "note_management_app"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "note_management_app"),
        "HOST": os.environ.get("SQL_HOST", "0.0.0.0"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "core.User"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_URL = "/staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Rest framework config
REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "exceptions_hog.exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework.authentication.TokenAuthentication",),
}

# Exception hog config
EXCEPTIONS_HOG = {
    "EXCEPTION_REPORTING": "exceptions_hog.handler.exception_reporter",
    "ENABLE_IN_DEBUG": False,
    "NESTED_KEY_SEPARATOR": "__",
    "SUPPORT_MULTIPLE_EXCEPTIONS": False,
}

# Swagger config
DRF_AUTH_TOKEN = {"DRF auth token": {"type": "apiKey", "name": "Authorization", "in": "header"}}
SWAGGER_SETTINGS = {"SECURITY_DEFINITIONS": {**DRF_AUTH_TOKEN}}

LOGIN_URL = "/admin/"

# CORS Config
CORS_ALLOWED_ORIGINS = list(set(os.environ.get("CORS_ALLOWED_ORIGINS", "http://localhost:8000").split("&")))
