import os

# Google OAuth2 settings
SOCIAL_AUTH_GOOGLE_OAUTH2_USE_UNIQUE_USER_ID = True
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("GOOGLE_OAUTH2_SECRET")


SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = [
    ("id", "id"),
    ("email", "email"),
    ("name", "name"),
    ("picture", "picture"),
    ("given_name", "given_name"),
    ("family_name", "family_name"),
]
