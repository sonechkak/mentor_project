import pytest

from django.core.exceptions import ValidationError

from src.apps.accounts.validators import SpecialSymbolValidator


@pytest.fixture
def validator():
    return SpecialSymbolValidator()


@pytest.mark.parametrize(
    "password, should_raise, expected_error",
    [
        ("Password!123", False, None),
        ("!@#1234", False, None),
        ("Password123", True, "Пароль должен содержать хотя бы один спец. символ."),
        ("12345", True, "Пароль должен содержать хотя бы один спец. символ."),
    ],
)
def test_special_symbol_validator(validator, password, should_raise, expected_error):
    """
    Проверяем работу валидатора с разными входными значениями.
    """
    if should_raise:
        with pytest.raises(ValidationError) as exc_info:
            validator.validate(password)
        assert exc_info.value.messages == [expected_error]
    else:
        try:
            validator.validate(password)
        except ValidationError:
            pytest.fail("ValidationError не должен был быть вызван для пароля с спецсимволом.")
