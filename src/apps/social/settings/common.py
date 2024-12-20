import os

# OAuth2 settings
SOCIAL_AUTH_USER_MODEL = 'accounts.User'
SOCIAL_AUTH_URL_NAMESPACE = "social"
SOCIAL_AUTH_POSTGRES_JSONFIELD = True
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "accounts:profile"
SOCIAL_AUTH_LOGIN_ERROR_URL = "accounts:login"

# Authentication backends
AUTHENTICATION_BACKENDS = [
    "social_core.backends.google.GoogleOAuth2",
    # "social_core.backends.github.GithubOAuth2",
    # "social_core.backends.vk.VKOAuth2",
    # "social_core.backends.telegram.TelegramAuth",
    "django.contrib.auth.backends.ModelBackend",
]

# Pipeline settings
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'apps.social.pipelines.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

# Убедитесь что эти настройки присутствуют
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = [
    ('id', 'id'),
    ('email', 'email'),
    ('name', 'name'),
    ('picture', 'picture'),
    ('given_name', 'given_name'),
    ('family_name', 'family_name'),
]
