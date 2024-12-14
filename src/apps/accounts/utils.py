import os


def avatar_upload_to(instance, filename):
    return os.path.join('src/media/avatars', filename)


def normalize_email(email: str) -> str:
    return email.lower()
