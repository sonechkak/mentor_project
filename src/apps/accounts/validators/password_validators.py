from .validators_user_model import (
    NotEmptyValidator,
    MinimumLengthValidator,
    UppercaseLetterValidator,
    NumericCharacterValidator,
    SpecialSymbolValidator,
)

# Список экземпляров валидаторов для паролей
PASSWORD_VALIDATORS = [
    NotEmptyValidator(),
    MinimumLengthValidator(),
    UppercaseLetterValidator(),
    NumericCharacterValidator(),
    SpecialSymbolValidator(),
]
