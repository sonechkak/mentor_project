import pytest

from rest_framework.test import APIRequestFactory

from apps.accounts.serializers import UserUpdateSerializer


@pytest.mark.django_db
class TestUserUpdateSerializer:
    def test_user_update_serializer_duplicate_email(self,
                                                    user_model,
                                                    user,
                                                    user_data_valid_for_serializer):
        another_user = user_model.objects.create_user(
            first_name="Another User",
            email="another@example.com",
            password="Anotherpassword123/*-"
        )

        user_data_valid_for_serializer["email"] = another_user.email
        serializer = UserUpdateSerializer(instance=user,
                                          data=user_data_valid_for_serializer)

        assert not serializer.is_valid()
        assert "email" in serializer.errors
        assert serializer.errors["email"][0] == "Пользователь с таким email уже существует."

    def test_user_update_serializer_update_by_regular_user(self,
                                                           current_user,
                                                           user,
                                                           user_data_valid_for_serializer,
                                                           api_client):
        # Обычный пользователь не может изменять is_admin и is_active
        user_data_valid_for_serializer["is_admin"] = True
        user_data_valid_for_serializer["is_active"] = False

        print("Admin: ", user.is_admin)

        # Создаем запрос от текущего пользователя (не админа)
        factory = APIRequestFactory()
        request = factory.get("/")  # Создаем фиктивный запрос
        request.user = current_user
        # print(request)
        # request["user"] = {}
        # request.user["is_authenticated"] = True
        # request.user["is_admin"] = False
        # print(request.user)
        # print("Admin: ", request.user.is_admin)  # False

        serializer = UserUpdateSerializer(instance=user,
                                          data=user_data_valid_for_serializer,
                                          context={"request": request})
        assert serializer.is_valid(), serializer.errors

        updated_user = serializer.save()
        assert updated_user.is_admin is False  # Обычный пользователь не может изменить is_admin
        assert updated_user.is_active is True  # Обычный пользователь не может изменить is_active
