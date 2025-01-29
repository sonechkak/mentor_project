from django.contrib.auth import get_user_model

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, generics, viewsets

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiTypes

from apps.accounts.serializers import (
    UserSerializer,
    UserListSerializer,
    UserChangePasswordSerializer,
)
from apps.core.permissions.admin import IsSuperuserStaffAdmin
from apps.core.paginations.pagination_factory import get_pagination_class
from apps.core.decorators.decorators import log_request_operations

User = get_user_model()


@extend_schema_view(
    post=extend_schema(
        summary="Регистрация нового пользователя в системе",
        tags=["Аутентификация & Авторизация"],
        operation_id="register user",
        request=UserSerializer,
    ),
    get=extend_schema(
        summary="Получить список всех пользователей",
        tags=["Аутентификация & Авторизация"],
        operation_id="get all users",
        request=UserListSerializer,
    ),
)
class UserListCreateView(generics.ListCreateAPIView, generics.UpdateAPIView):
    queryset = User.objects.all()
    pagination_class = get_pagination_class()

    def get(self, request, *args, **kwargs):
        """Метод для получения списка пользователей"""
        return super().get(request, *args, **kwargs)

    @log_request_operations(logger_name="accounts")
    def post(self, request, *args, **kwargs):
        """Метод для регистрации пользователя"""

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={"status": "success", "message": "Пользователь успешно зарегистрирован."},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data={"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get_permissions(self):
        """Переопределяем get_permissions, чтобы использовать разные права доступа для POST и GET"""
        permissions = [AllowAny] if self.request.method == "POST" else [IsSuperuserStaffAdmin]
        self.permission_classes = permissions
        return super().get_permissions()

    def get_serializer_class(self):
        return UserSerializer if self.request.method == "POST" else UserListSerializer


@extend_schema_view(
    patch=extend_schema(
        summary="Обновление пароля пользователя по id",
        tags=["Аутентификация & Авторизация"],
        operation_id="update password",
        request=UserChangePasswordSerializer,
    )
)
class UserChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserChangePasswordSerializer
    permission_classes = [IsSuperuserStaffAdmin]
    lookup_field = "id"
    http_method_names = ["patch"]

    @log_request_operations(logger_name="accounts")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


@extend_schema_view(
    delete=extend_schema(
        summary="Удаление пользователя по id",
        tags=["Аутентификация & Авторизация"],
        operation_id="delete user",
        request=None,
        responses={204: OpenApiTypes.NONE},
    )
)
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsSuperuserStaffAdmin]
    lookup_field = "id"

    @log_request_operations(logger_name="accounts")
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
