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
    is_active = serializers.BooleanField(default=True)
    is_admin = serializers.BooleanField(default=False)
    first_name = serializers.CharField(validators=[NotEmptyValidator(), NameValidator()])
    email = serializers.EmailField(validators=[EmailValidator()])
    password = serializers.CharField(
        write_only=True,
        validators=[validator.validate for validator in PASSWORD_VALIDATORS]
    )
    avatar = serializers.ImageField(
        required=False,
        validators=[ImageValidator(file_extension=['jpg', 'png'])],
    )
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "date_joined",
            "last_login",
            "is_active",
            "is_admin",
            "avatar"
        ]

    def validate_email(self, value: str) -> str:
        email = normalize_email(value)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Пользователь с таким Email уже существует.")
        return value

    def create(self, validated_data: dict) -> User:
        request = self.context.get("request")
        is_admin_request = request and request.user.is_authenticated and request.user.is_admin

        if is_admin_request:
            if validated_data.get("is_admin", False):
                user = User.objects.create_superuser(**validated_data)
            else:
                user = User.objects.create_user(**validated_data)

        else:
            validated_data["is_active"] = True
            validated_data["is_admin"] = False
            user = User.objects.create_user(**validated_data)

        return user


class UserUpdateSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ["id", "first_name", "last_name", "email", "is_active", "is_admin", "avatar"]

    def validate_email(self, value: str) -> str:
        email = normalize_email(value)
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return email

    def update(self, instance, validated_data: dict) -> User:
        for attr, value in validated_data.items():
            try:
                setattr(instance, attr, value)
            except AttributeError:
                pass

        self.set_user_permissions_based_on_request(instance=instance, validated_data=validated_data)
        instance.save()
        return instance

    def set_user_permissions_based_on_request(self, instance, validated_data: dict) -> None:
        request = self.context.get("request")
        is_admin_request = request and request.user.is_authenticated and request.user.is_admin

        if is_admin_request:
            instance.is_admin = validated_data.get("is_admin", instance.is_admin)
            instance.is_active = validated_data.get("is_active", instance.is_active)
            instance.is_staff = instance.is_admin
            instance.is_superuser = instance.is_admin
        else:
            instance.is_active = True
            instance.is_admin = False
            instance.is_staff = False
            instance.is_superuser = False


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        validators=[validator.validate for validator in PASSWORD_VALIDATORS], write_only=True
    )

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
            instance.save()
        return instance
