from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from rest_framework import serializers

from apps.accounts.utils import normalize_email
from apps.accounts.validators import (
    NameValidator,
    PASSWORD_VALIDATORS,
    NotEmptyValidator,
    EmailValidator,
)

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    extra_kwargs = {
        "first_name": {"validators": [NotEmptyValidator().validate, NameValidator().validate]},
        "email": {"validators": [NotEmptyValidator().validate, EmailValidator().validate]},
        "password": {
            "validators": [validator.validate for validator in PASSWORD_VALIDATORS],
            "write_only": True,
            "required": True,
            "style": {"input_type": "password"},
        },
    }

    class Meta:
        model = User
        fields = ["first_name", "email", "password"]

    def validate_email(self, value: str) -> str:
        email = normalize_email(value)
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким Email уже существует.")
        return value

    def create(self, validated_data: dict) -> User:
        user = User.objects.create_user(**validated_data)
        return user
