import os

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator, FileExtensionValidator
from django.db import models
from django.core.exceptions import ValidationError

from PIL import Image


name_validators = [
    MinLengthValidator(2, "Поле должно содержать минимум 2 символа."),
    RegexValidator(
        regex="^[a-zA-Zа-яА-ЯёЁ]+$",
        message="Поле может содержать только буквы латиницы и кириллицы.",
    ),
]

email_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    message='Email должен содержать только буквы латиницы, цифры, спец. символы, но без пробелов.'
)

password_validators = [
    MinLengthValidator(8, "Пароль должен содержать минимум 8 символов."),
    RegexValidator(
        regex=r'[A-Z]',
        message="Пароль должен содержать хотя бы одну заглавную букву."
    ),
    RegexValidator(
        regex=r'\d',
        message="Пароль должен содержать хотя бы одну цифру."
    ),
    RegexValidator(
        regex=r'[!@#$%^&*(),.?":{}|<>]',
        message="Пароль должен содержать хотя бы один спец. символ."
    )
]


def avatar_upload_to(instance, filename):
    return os.path.join('avatars', filename)


def validate_image_size(image):
    file_size = image.file.size
    if file_size > 2 * 1024 * 1024:
        raise ValidationError("Размер файла не должен превышать 2MB.")

    # Проверка на максимальный размер изображения (300x300 px)
    img = Image.open(image)
    if img.height > 300 or img.width > 300:
        raise ValidationError("Размер изображения не должен превышать 300x300 пикселей.")


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен для создания пользователя.")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    first_name = models.CharField(
        max_length=30,
        validators=name_validators,
    )
    last_name = models.CharField(
        max_length=30,
        blank=True,
        validators=name_validators,
    )
    email = models.EmailField(
        unique=True,
        max_length=100,
        validators=[email_validator],
        error_messages={
            'invalid': 'Введите правильный адрес электронной почты.'
        }
    )
    password = models.CharField(
        max_length=128,
        validators=password_validators,
    )
    avatar = models.ImageField(
        upload_to=avatar_upload_to,
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'png']),
            validate_image_size,  # Валидация размера файла и изображения
        ]
    )
    # ??? Удаляем поле username, если оно не нужно  ???
    username = None
    # Какие еще поля нужны???

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name} <{self.email}>'

