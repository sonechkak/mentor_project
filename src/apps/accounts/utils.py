import os

from django.core.exceptions import ValidationError


def avatar_upload_to(instance, filename: str) -> str:
    if not filename:
        raise ValidationError("Имя файла не может быть пустым или None")
    return os.path.join('avatars', filename)


def normalize_email(email: str) -> str:
    return email.lower()
