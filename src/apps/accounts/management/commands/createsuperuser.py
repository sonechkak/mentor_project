from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from getpass import getpass


class Command(BaseCommand):
    help = "Создать суперпользователя с кастомной валидацией полей"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Создание суперпользователя"))

        first_name = self.get_field_input("first_name", "Имя")
        email = self.get_field_input("email", "Email")

        password1 = self.get_password_from_cli()
        password2 = self.get_password_from_cli(label="Введите повторно пароль: ")
        while password1 != password2:
            self.stderr.write("Пароли не совпадают. Попробуйте снова.\n")
            password1 = self.get_password_from_cli()
            password2 = self.get_password_from_cli(label="Введите повторно пароль: ")

        # Создание суперпользователя
        User = get_user_model()
        user = User.objects.create_superuser(first_name=first_name, email=email, password=password1)
        self.stdout.write(self.style.SUCCESS(f"Суперпользователь  [ {user} ] успешно создан!"))

    def get_field_input(self, field_name: str, field_label: str) -> str:
        """
        Общая функция для ввода и валидации данных.
        """
        while True:
            value = input(f"{field_label}: ").strip()
            try:
                self.validate_field(field_name, value)
                return value
            except ValidationError as e:
                self.stderr.write(f"Ошибка валидации поля <{field_label}>: {e.message}")
                self.stderr.write("Попробуйте ввести снова.\n")

    def validate_field(self, field_name: str, value: str) -> None:
        """
        Вызывает кастомные валидаторы модели User для конкретного поля.
        """
        # Получаем все валидаторы для поля из модели
        User = get_user_model()
        field = User._meta.get_field(field_name)
        for validator in field.validators:
            validator(value)

    def get_password_from_cli(self, label: str = "Пароль: ") -> str:
        """
        Возвращает пароль с подтверждением через консоль.
        """
        while True:
            password = getpass(f"{label}").strip()
            try:
                self.validate_field("password", password)
                break
            except ValidationError as e:
                self.stderr.write(f"Ошибка валидации пароля: {e.message}")
                self.stderr.write("Попробуйте ввести пароль снова.\n")

        return password
