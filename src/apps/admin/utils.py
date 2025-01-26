import string
from random import choices, choice


def normalize_email(email: str) -> str:
    return email.lower()


def generate_password(
    min_length_password: int = 8, max_length_password: int = 128, length_password: int = 8
) -> str:
    """
    Возвращает сгенерированный пароль длиной length_password. По умолчанию length_password=8.
    """
    if not (min_length_password <= length_password <= max_length_password):
        raise ValueError(
            f"Длина пароля должна быть от {min_length_password} до {max_length_password} символов."
        )

    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    special = string.punctuation
    all_characters = lower + upper + digits + special

    password = [choice(lower), choice(upper), choice(digits), choice(special)]

    password.extend(choices(all_characters, k=length_password - 4))

    return "".join(password)
