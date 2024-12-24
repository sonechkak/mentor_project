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

load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "True")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")


THIRD_PARTY_APPS = [
    "rest_framework",
    "social_django",
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
]

INSTALLED_APPS = THIRD_PARTY_APPS + DJANGO_APPS + LOCAL_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
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
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication settings
# если не авторизован
LOGIN_URL = 'accounts:login'
# после входа
LOGIN_REDIRECT_URL = 'accounts:home'
LOGOUT_URL = 'accounts:logout'
LOGOUT_REDIRECT_URL = 'accounts:login'
