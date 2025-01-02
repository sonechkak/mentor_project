from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager
from .validators import (
    NameValidator,
    EmailValidator,
    ImageValidator,
    NotEmptyValidator,
    PASSWORD_VALIDATORS,
)
from .utils import avatar_upload_to


class User(AbstractUser):
    first_name = models.CharField(
        verbose_name="Имя",
        validators=[NotEmptyValidator().validate, NameValidator().validate],
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        blank=True,
        validators=[NotEmptyValidator().validate, NameValidator().validate],
    )
    email = models.EmailField(
        verbose_name="Email",
        unique=True,
        validators=[NotEmptyValidator().validate, EmailValidator().validate],
    )
    password = models.CharField(
        verbose_name="Пароль",
        validators=[validator.validate for validator in PASSWORD_VALIDATORS],
    )
    avatar = models.ImageField(
        verbose_name="Аватар",
        upload_to=avatar_upload_to,
        blank=True,
        validators=[ImageValidator().validate],
    )
    is_admin = models.BooleanField(verbose_name="Администратор", default=False)
    username = None

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    class Meta:
        app_label = "accounts"
        db_table = "accounts_user"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("id",)

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"
