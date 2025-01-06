import os

# OAuth2 settings
SOCIAL_AUTH_USER_MODEL = "accounts.User"
SOCIAL_AUTH_URL_NAMESPACE = "social"
SOCIAL_AUTH_POSTGRES_JSONFIELD = True
# редирект после успешной авторизации
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "accounts:home"
# редирект в случае ошибки
SOCIAL_AUTH_LOGIN_ERROR_URL = "accounts:login"
SOCIAL_AUTH_RAISE_EXCEPTIONS = False
SOCIAL_AUTH_ALLOW_EMPTY_EMAIL = True

# Authentication backends
AUTHENTICATION_BACKENDS = [
    "social_core.backends.google.GoogleOAuth2",
    "social_core.backends.github.GithubOAuth2",
    "social_core.backends.vk.VKOAuth2",
    "social_core.backends.telegram.TelegramAuth",
    "django.contrib.auth.backends.ModelBackend",
]

# Pipeline settings
SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "apps.social.pipelines.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)

# Настройки CSP
CSP_DEFAULT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'", "https://telegram.org", "https://oauth.telegram.org")
CSP_FRAME_ANCESTORS = ("'self'", "https://oauth.telegram.org")
CSP_FRAME_SRC = ("'self'", "https://oauth.telegram.org")
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'", "https://telegram.org")
CSP_CONNECT_SRC = ("'self'", "https://oauth.telegram.org")
