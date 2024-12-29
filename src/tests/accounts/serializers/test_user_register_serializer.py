import pytest

from apps.accounts.serializers import UserRegistrationSerializer


@pytest.mark.django_db
class TestUserRegistrationSerializer:
    def test_valid_data(self, user_data_valid_for_serializer, user_model):
        """Тест на успешную валидацию данных"""
        serializer = UserRegistrationSerializer(data=user_data_valid_for_serializer)
        assert serializer.is_valid()
        user = serializer.save()
        assert user_model.objects.filter(email="user@example.com").exists()
        assert user.first_name == "User"
        assert user.check_password("Userpassword123/*-")

    def test_duplicate_email(self, user, user_data_valid_for_serializer):
        """Тест на проверку существующего email"""
        duplicate_email_serializer = UserRegistrationSerializer(data=user_data_valid_for_serializer)
        assert not duplicate_email_serializer.is_valid()
        assert "email" in duplicate_email_serializer.errors
        assert (
            "Пользователь с таким Email уже существует."
            in duplicate_email_serializer.errors["email"]
        )

    def test_empty_first_name(self, user_data_valid_for_serializer):
        """Тест на пустое поле first_name"""
        user_data_valid_for_serializer["first_name"] = ""
        serializer = UserRegistrationSerializer(data=user_data_valid_for_serializer)
        assert not serializer.is_valid()
        assert "first_name" in serializer.errors

    def test_empty_email(self, user_data_valid_for_serializer):
        """Тест на пустое поле email"""
        user_data_valid_for_serializer["email"] = ""
        serializer = UserRegistrationSerializer(data=user_data_valid_for_serializer)
        assert not serializer.is_valid()
        assert "email" in serializer.errors

    def test_empty_password(self, user_data_valid_for_serializer):
        """Тест на пустое поле email"""
        user_data_valid_for_serializer["password"] = ""
        serializer = UserRegistrationSerializer(data=user_data_valid_for_serializer)
        assert not serializer.is_valid()
        assert "password" in serializer.errors
