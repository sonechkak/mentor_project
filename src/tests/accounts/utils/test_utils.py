import os

from django.core.exceptions import ValidationError

import pytest

from src.apps.accounts.utils import avatar_upload_to, normalize_email


@pytest.mark.parametrize(
    "filename, expected_path",
    [
        ("profile_pic.jpg", os.path.join('avatars', 'profile_pic.jpg')),
        ("avatar.png", os.path.join('avatars', 'avatar.png')),
        ("image_123.png", os.path.join('avatars', 'image_123.png')),
        # Невалидные случаи
        ("", "avatars/"),
        (None, "avatars/"),
    ]
)
def test_avatar_upload_to(filename, expected_path):
    if filename is None or filename == "":
        with pytest.raises(ValidationError):
            avatar_upload_to(None, filename)
    else:
        assert avatar_upload_to(None, filename) == expected_path


@pytest.mark.parametrize(
    "input_email, expected_email",
    [
        ("USER@EXAMPLE.COM", "user@example.com"),
        ("First.Last@Example.com", "first.last@example.com"),
        ("alreadylower@example.com", "alreadylower@example.com"),
        ("UPPERCASE@DOMAIN.COM", "uppercase@domain.com"),
    ]
)
def test_normalize_email(input_email, expected_email):
    assert normalize_email(input_email) == expected_email
