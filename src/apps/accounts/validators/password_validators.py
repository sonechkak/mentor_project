from .validators_user_model import (
    NotEmptyValidator,
    MinMaxLengthPasswordValidator,
    UppercaseLetterValidator,
    NumericCharacterValidator,
    SpecialSymbolValidator,
)

# Список экземпляров валидаторов для паролей
PASSWORD_VALIDATORS = [
    NotEmptyValidator(),
    MinMaxLengthPasswordValidator(),
    UppercaseLetterValidator(),
    NumericCharacterValidator(),
    SpecialSymbolValidator(),
]
