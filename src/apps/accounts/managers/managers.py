from typing import TYPE_CHECKING

from django.contrib.auth.base_user import BaseUserManager

if TYPE_CHECKING:
    from src.apps.accounts.models import User


class CustomUserManager(BaseUserManager):
    def create_user(self, first_name: str, email: str, password: str, **extra_fields) -> "User":
        if not first_name:
            raise ValueError("Имя обязательно для создания пользователя.")

        if not email:
            raise ValueError("Email обязателен для создания пользователя.")

        if not password:
            raise ValueError("Пароль обязателен для создания пользователя.")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)

        user = self.model(first_name=first_name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, first_name: str, email: str, password: str, **extra_fields
    ) -> "User":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")
        if not extra_fields.get("is_admin"):
            raise ValueError("Администратор должен иметь is_admin=True.")

        return self.create_user(first_name, email, password, **extra_fields)
