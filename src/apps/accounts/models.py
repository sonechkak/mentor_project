from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models

from .managers.managers import CustomUserManager
from .validators.validators_user_model import (
    name_validators,
    email_validator,
    password_validators,
    validate_image_size
)
from .utils import avatar_upload_to


class User(AbstractUser):
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=30,
        validators=name_validators,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=30,
        blank=True,
        validators=name_validators,
    )
    email = models.EmailField(
        verbose_name="Email",
        unique=True,
        max_length=100,
        validators=[email_validator],
        error_messages={
            'invalid': 'Введите правильный адрес электронной почты.'
        }
    )
    password = models.CharField(
        verbose_name="Пароль",
        max_length=128,
        validators=password_validators,
    )
    avatar = models.ImageField(
        verbose_name="Аватар",
        upload_to=avatar_upload_to,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'png']),
            validate_image_size,  # Валидация размера файла и изображения
        ]
    )
    is_admin = models.BooleanField(
        verbose_name="Администратор",
        default=False
    )
    username = None

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f'{self.first_name} {self.last_name} <{self.email}>'
