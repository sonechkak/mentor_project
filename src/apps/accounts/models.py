from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager
from .validators import (
    SpecialSymbolValidator,
    UppercaseLetterValidator,
    NumericCharacterValidator,
    NameValidator,
    EmailValidator,
    ImageValidator,
    MinimumLengthValidator,
    NotEmptyValidator,
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
        validators=[
            NotEmptyValidator().validate,
            NameValidator().validate,
        ],
    )
    email = models.EmailField(
        verbose_name="Email",
        unique=True,
        validators=[
            NotEmptyValidator().validate,
            EmailValidator().validate,
        ],
    )
    password = models.CharField(
        verbose_name="Пароль",
        validators=[
            NotEmptyValidator().validate,
            MinimumLengthValidator().validate,
            UppercaseLetterValidator().validate,
            NumericCharacterValidator().validate,
            SpecialSymbolValidator().validate,
        ],
    )
    avatar = models.ImageField(
        verbose_name="Аватар",
        upload_to=avatar_upload_to,
        blank=True,
        validators=[
            ImageValidator().validate,
        ],
    )
    is_admin = models.BooleanField(verbose_name="Администратор", default=False)
    username = None

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"
