import pytest

from apps.accounts.serializers import UserSerializer


@pytest.mark.django_db
class TestUserRegistrationSerializer:
    def test_user_serializer_with_valid_data(self, user_data_valid_for_serializer):
        """Тест на успешную валидацию данных"""
        serializer = UserSerializer(data=user_data_valid_for_serializer)
        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data["email"] == user_data_valid_for_serializer["email"]
        assert serializer.validated_data["first_name"] == user_data_valid_for_serializer[
            "first_name"]

    def test_user_serializer_create_user(self, user_data_valid_for_serializer, user_model):
        """Тест для создания обычного пользователя"""
        serializer = UserSerializer(data=user_data_valid_for_serializer)
        assert serializer.is_valid(), serializer.errors
        user = serializer.save()
        assert user_model.objects.filter(email=user_data_valid_for_serializer["email"]).exists()
        assert user.first_name == "User"
        assert user.check_password("Userpassword123/*-")
        assert user.is_admin is False
        assert user.is_active is True

    def test_user_serializer_create_admin(self,
                                          user_data_valid_for_serializer,
                                          user_model,
                                          api_client):
        admin_user = user_model.objects.create_superuser(
            email="admin@example.com",
            password="adminpassword123",
            first_name="Admin"
        )
        api_client.force_authenticate(user=admin_user)
        request = api_client.request()
        request.user = admin_user

        user_data_valid_for_serializer["is_admin"] = True
        serializer = UserSerializer(data=user_data_valid_for_serializer,
                                    context={"request": request})
        assert serializer.is_valid(), serializer.errors
        user = serializer.save()
        assert user_model.objects.filter(email=user_data_valid_for_serializer["email"]).exists()
        assert user.is_admin is True

    def test_duplicate_email(self, user, user_data_valid_for_serializer):
        """Тест на проверку существующего email"""
        duplicate_email_serializer = UserSerializer(data=user_data_valid_for_serializer)
        assert not duplicate_email_serializer.is_valid()
        assert "email" in duplicate_email_serializer.errors
        assert (
            "Пользователь с таким Email уже существует."
            in duplicate_email_serializer.errors["email"]
        )

    def test_empty_first_name(self, user_data_valid_for_serializer):
        """Тест на пустое поле first_name"""
        user_data_valid_for_serializer["first_name"] = ""
        serializer = UserSerializer(data=user_data_valid_for_serializer)
        assert not serializer.is_valid()
        assert "first_name" in serializer.errors

    def test_empty_email(self, user_data_valid_for_serializer):
        """Тест на пустое поле email"""
        user_data_valid_for_serializer["email"] = ""
        serializer = UserSerializer(data=user_data_valid_for_serializer)
        assert not serializer.is_valid()
        assert "email" in serializer.errors

    def test_empty_password(self, user_data_valid_for_serializer):
        """Тест на пустое поле email"""
        user_data_valid_for_serializer["password"] = ""
        serializer = UserSerializer(data=user_data_valid_for_serializer)
        assert not serializer.is_valid()
        assert "password" in serializer.errors

    def test_user_serializer_read_only_fields(self, user_data_valid_for_serializer):
        user_data_valid_for_serializer["date_joined"] = "2023-01-01T00:00:00Z"
        user_data_valid_for_serializer["last_login"] = "2023-01-01T00:00:00Z"
        serializer = UserSerializer(data=user_data_valid_for_serializer)
        assert serializer.is_valid(), serializer.errors
        assert "date_joined" not in serializer.validated_data
        assert "last_login" not in serializer.validated_data
