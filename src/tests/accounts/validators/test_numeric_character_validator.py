import pytest

from django.core.exceptions import ValidationError

from src.apps.accounts.validators import NumericCharacterValidator


@pytest.fixture
def validator():
    return NumericCharacterValidator()


@pytest.mark.parametrize(
    "value, should_raise, expected_error",
    [
        ("password", True, "Пароль должен содержать хотя бы одну цифру."),
        ("lowerc/*-+QWDQE", True, "Пароль должен содержать хотя бы одну цифру."),
        ("    ", True, "Пароль должен содержать хотя бы одну цифру."),
        ("", True, "Пароль должен содержать хотя бы одну цифру."),
        ("1234Password", False, None),
        ("1", False, None),
    ]
)
def test_numeric_character_validator(validator, value, should_raise, expected_error):
    """
    Проверяем работу валидатора с разными входными значениями.
    """
    if should_raise:
        with pytest.raises(ValidationError) as exc_info:
            validator.validate(value)
        assert exc_info.value.messages == [expected_error]
    else:
        try:
            validator.validate(value)
        except ValidationError:
            pytest.fail("ValidationError не должен быть вызван для пароля с цифрой")
