from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, email, password=None, **extra_fields):
        if not first_name:
            raise ValueError("Имя обязательно для создания пользователя.")

        if not email:
            raise ValueError("Email обязателен для создания пользователя.")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)

        user = self.model(first_name=first_name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")
        if not extra_fields.get("is_admin"):
            raise ValueError("Администратор должен иметь is_admin=True.")

        self.validate_field("first_name", first_name)
        self.validate_field("email", email)
        self.validate_field("password", password)

        return self.create_user(first_name, email, password, **extra_fields)

    def validate_field(self, field_name, value):
        """
        Вызывает кастомные валидаторы модели User для конкретного поля.
        """
        User = get_user_model()
        field = User._meta.get_field(field_name)
        for validator in field.validators:
            validator(value)
