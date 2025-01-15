import os
import sys
from pathlib import Path
from dotenv import load_dotenv

from apps.social.settings.common import *  # noqa
from apps.social.settings.google import *  # noqa
from apps.social.settings.github import *  # noqa
from apps.social.settings.vk import *  # noqa
from apps.social.settings.telegram import *  # noqa

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "True")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")

THIRD_PARTY_APPS = [
    "rest_framework",
    "social_django",
    "drf_spectacular",
    'django_filters',
    "django_extensions",
]

DJANGO_APPS = [
    "accounts",
    # 'django.contrib.admin',
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

AUTH_USER_MODEL = "accounts.User"

LOCAL_APPS = [
    "blog",
    "admin",
    "social",
    "api",
    "core",
]

INSTALLED_APPS = THIRD_PARTY_APPS + DJANGO_APPS + LOCAL_APPS

MIDDLEWARE = [
    # "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.app.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "accounts.validators.validators_user_model.NotEmptyValidator",
    },
    {
        "NAME": "accounts.validators.validators_user_model.MinimumLengthValidator",
    },
    {
        "NAME": "accounts.validators.validators_user_model.UppercaseLetterValidator",
    },
    {
        "NAME": "accounts.validators.validators_user_model.SpecialSymbolValidator",
    },
    {
        "NAME": "accounts.validators.validators_user_model.NumericCharacterValidator",
    },
]

LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Database
POSTGRES_EXTENSIONS = ['pg_trgm']

# Authentication settings
# если не авторизован
LOGIN_URL = "accounts:login"
# после входа
LOGIN_REDIRECT_URL = "accounts:home"
LOGOUT_URL = "accounts:logout"
LOGOUT_REDIRECT_URL = "accounts:login"

#  REST_FRAMEWORK
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FileUploadParser",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# DRF SPECTACULAR
SPECTACULAR_SETTINGS = {
    "TITLE": "Mentor project",
    "DESCRIPTION": "Mentor project",
    "VERSION": "1.0.0",
    "SERVE_PERMISSIONS": [
        "apps.core.permissions.admin.IsSuperuserStaffAdmin",
    ],
    "SERVE_AUTHENTICATION": [
        "rest_framework.authentication.BasicAuthentication",
    ],
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "displayOperationId": True,
        "syntaxHighlight.active": True,
        "syntaxHighlight.theme": "arta",  # monokai, agate
        "defaultModelsExpandDepth": -1,
        "displayRequestDuration": True,
        "filter": True,
        "requestSnippetsEnabled": False,
    },
    "COMPONENT_SPLIT_REQUEST": True,
    "SORT_OPERATIONS": False,
    # 'ENABLE_DJANGO_DEPLOY_CHECK': False,
    # 'DISABLE_ERRORS_AND_WARNINGS': True,
}

# LOGGING
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "file_formatter": {
            "format": "{asctime} | {levelname} | {pathname} line:{lineno} | {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "console_formatter": {
            "format": "{asctime} {message}",
            "style": "{",
            "datefmt": "%H:%M:%S",
        },
    },
    "handlers": {
        # Общий обработчик для записи в файл common.log с ротацией
        "common_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "common.log",
            "maxBytes": 1024 * 1024 * 10,  # 10 MB
            "backupCount": 5,  # Сохраняем последние 5 файлов
            "formatter": "console_formatter",
        },
        # Обработчик для записи логов приложения "accounts"
        "accounts_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "accounts.log",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 3,  # Сохраняем последние 3 файла
            "formatter": "file_formatter",
        },
        # Обработчик для записи логов приложения "accounts"
        "admin_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "admin.log",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 3,  # Сохраняем последние 3 файла
            "formatter": "file_formatter",
        },
        # Обработчик для вывода в консоль
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "console_formatter",
        },
    },
    "loggers": {
        "accounts": {
            "handlers": ["accounts_file"],
            "level": "INFO",
            "propagate": False,  # Важно! Не нужно передавать сообщения в стандартный логгер Django
        },
        "admin": {
            "handlers": ["admin_file"],
            "level": "INFO",
            "propagate": False,  # Важно! Не нужно передавать сообщения в стандартный логгер Django
        },
        "django": {
            "handlers": ["console", "common_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
