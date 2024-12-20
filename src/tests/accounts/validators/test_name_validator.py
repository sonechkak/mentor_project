import pytest

from django.core.exceptions import ValidationError

from src.apps.accounts.validators import NameValidator


@pytest.fixture
def validator():
    return NameValidator()


@pytest.mark.parametrize(
    "value, should_raise, expected_error",
    [
        # Невалидные значения (слишком короткие или длинные)
        ("", True, "Поле должно содержать минимум 2 символа."),
        ("a", True, "Поле должно содержать минимум 2 символа."),
        ("a" * 31, True, "Поле должно содержать максимум 30 символов."),
        # Невалидные значения (содержат недопустимые символы)
        ("John123", True, "Поле может содержать только буквы латиницы и кириллицы."),
        ("Иван123", True, "Поле может содержать только буквы латиницы и кириллицы."),
        ("John@Doe", True, "Поле может содержать только буквы латиницы и кириллицы."),
        # Валидные значения
        ("Иван", False, None),
        ("John", False, None),
        ("Александр", False, None),
        ("Maria", False, None),
    ],
)
def test_name_validator(validator, value, should_raise, expected_error):
    """
    Проверяем работу валидатора для имени с разными входными значениями.
    """
    if should_raise:
        with pytest.raises(ValidationError) as exc_info:
            validator.validate(value)
        assert exc_info.value.messages == [expected_error]
    else:
        try:
            validator.validate(value)
        except ValidationError:
            pytest.fail("ValidationError не должен быть вызван для валидного значения.")
