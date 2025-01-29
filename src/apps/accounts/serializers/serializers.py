from django.contrib.auth import get_user_model

from rest_framework import serializers

from apps.accounts.utils import normalize_email
from apps.accounts.validators import (
    NameValidator,
    PASSWORD_VALIDATORS,
    NotEmptyValidator,
    EmailValidator,
    ImageValidator,
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "is_active", "is_admin"]
        extra_kwargs = {
            "first_name": {"validators": [NotEmptyValidator(), NameValidator()]},
            "email": {"validators": [NotEmptyValidator(), EmailValidator()]},
            "password": {
                "validators": [validator.validate for validator in PASSWORD_VALIDATORS],
                "write_only": True,
                "required": True,
                "style": {"input_type": "password"},
            },
            "is_admin": {"default": False},
            # "avatar": {
            #     "required": False,
            #     "allow_null": True,
            # },
        }

    def validate_email(self, value: str) -> str:
        email = normalize_email(value)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Пользователь с таким Email уже существует.")
        return value

    def validate_avatar(self, value):
        if value:
            ImageValidator().validate(value)
        return value

    def create(self, validated_data: dict) -> User:
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data: dict) -> User:
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.is_admin = validated_data.get("is_admin", instance.is_admin)

        if "password" in validated_data:
            instance.set_password(validated_data["password"])

        instance.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "date_joined",
            "last_login",
            "is_active",
        ]


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        validators=[validator.validate for validator in PASSWORD_VALIDATORS], write_only=True
    )

    def update(self, instance, validated_data):
        password = validated_data["password"]
        instance.set_password(password)
        instance.save()
        return instance
