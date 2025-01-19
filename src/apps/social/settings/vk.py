import os

# VK
SOCIAL_AUTH_VK_OAUTH2_KEY = os.getenv("VK_OAUTH2_KEY")
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.getenv("VK_OAUTH2_SECRET")
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ["email", "offline"]
SOCIAL_AUTH_VK_OAUTH2_API_VERSION = "5.131"
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
SOCIAL_AUTH_ALLOWED_REDIRECT_HOSTS = ["local-mentor-app.sonechkak.ru"]
SOCIAL_AUTH_VK_OAUTH2_EXTRA_DATA = ["email"]
SOCIAL_AUTH_INACTIVE_USER_LOGIN = False
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = False  # Будет использовать email как username
