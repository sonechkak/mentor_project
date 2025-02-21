import re

from django.core.exceptions import ValidationError


class SlugValidator:
    """
    Валидатор для проверки slug:
    - Только буквы латиницы, цифры и спецсимволы _-
    """

    def __init__(self) -> None:
        self.pattern = re.compile(r'^[a-z0-9_\-]+$')

    def __call__(self, value: str) -> None:
        self.validate(value)

    def validate(self, value: str) -> None:
        if not self.pattern.match(value):
            raise ValidationError(
                "Поле может содержать только строчные буквы (a-z), цифры (0-9) и символы (_-)"
            )


class LatinCyrillicValidator:
    """
    Валидатор для проверки поля на буквы латиницы и кириллицы:
    - Только буквы латиницы и кириллицы
    """

    def __init__(self) -> None:
        self.pattern = re.compile(r"^[a-zA-Zа-яА-ЯёЁ]+$")

    def __call__(self, value: str):
        self.validate(value)

    def validate(self, value: str) -> None:
        if not self.pattern.match(value):
            raise ValidationError("Поле может содержать только буквы латиницы и кириллицы.")


class MinMaxLengthValidator:
    """
    Валидатор для проверки поля указанной длины :
    """

    def __init__(self, min_length: int = 1, max_length: int = 30) -> None:
        self.min_length = min_length
        self.max_length = max_length

    def __call__(self, value: str):
        self.validate(value)

    def validate(self, value: str) -> None:
        if len(value) < self.min_length:
            raise ValidationError(f"Поле должен быть минимум {self.min_length} символов")

        if len(value) > self.max_length:
            raise ValidationError(f"Поле должен быть максимум {self.max_length} символов")