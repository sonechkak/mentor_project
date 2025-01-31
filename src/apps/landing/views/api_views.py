from rest_framework import generics, viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiTypes
from rest_framework.permissions import AllowAny

from landing.models import *
from landing.serializers.serializers import *

from apps.core.permissions import IsSuperuserStaffAdmin


@extend_schema_view(
    get=extend_schema(
        summary="Получить список всех блоков Главное",
        tags=["Лендинг.Главная"],
        operation_id="get all main inf",
        request=MainInfSerializer,
    ),
)
class MainInfAPIViews(generics.ListAPIView):
    queryset = MainInf.objects.all()
    serializer_class = MainInfSerializer

@extend_schema_view(
    list=extend_schema(
        summary="Получить список всех блоков Обо мне",
        tags=["Лендинг.Обо Мне"],
        operation_id="get all about me",
        responses={200: AboutMeSerializer(many=True)},  # Список всех блоков
    ),
    create=extend_schema(
        summary="Создать новый блок Обо мне",
        tags=["Лендинг.Обо Мне"],
        operation_id="create new block about me",
        request=AboutMeSerializer,
        responses={201: AboutMeSerializer},  # Ответ с созданным объектом
    ),
    retrieve=extend_schema(
        summary="Получить блок Обо мне по его ID",
        tags=["Лендинг.Обо Мне"],
        operation_id="get one block about me",
        request=AboutMeSerializer,
        responses={201: AboutMeSerializer},  # Ответ с созданным объектом
    ),
    update=extend_schema(
        summary="Обновить один блок Обо мне по его ID",
        tags=["Лендинг.Обо Мне"],
        operation_id="update block about me",
        request=AboutMeSerializer,
        responses={200: AboutMeSerializer},  # Ответ с обновленным объектом
    ),
    destroy=extend_schema(
        summary="Удалить один блок Обо мне по его ID",
        tags=["Лендинг.Обо Мне"],
        operation_id="delete block about me",
        responses={204: None},  # Ответ с успешным удалением (нет содержимого)
    ),
)
class AboutMeViewSet(viewsets.ModelViewSet):
    queryset = AboutMe.objects.all()
    serializer_class = AboutMeSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_permissions(self):
        """Переопределяем get_permissions, чтобы использовать разные права доступа для POST и GET"""
        permissions = [AllowAny] if self.request.method == "GET" else [IsSuperuserStaffAdmin]
        self.permission_classes = permissions
        return super().get_permissions()


@extend_schema_view(
    list=extend_schema(
        summary="Получить список всех блоков Контента",
        tags=["Лендинг.Контент"],
        operation_id="get all contents",
        responses={200: ContentSerializer(many=True)},  # Список всех блоков
    ),
    create=extend_schema(
        summary="Создать новый блок Контента",
        tags=["Лендинг.Контент"],
        operation_id="create new block content",
        request=ContentSerializer,
        responses={201: ContentSerializer},  # Ответ с созданным объектом
    ),
    retrieve=extend_schema(
        summary="Получить блок Контента по его ID",
        tags=["Лендинг.Контент"],
        operation_id="get one block content",
        request=ContentSerializer,
        responses={201: ContentSerializer},  # Ответ с созданным объектом
    ),
    update=extend_schema(
        summary="Обновить один блок Контента по его ID",
        tags=["Лендинг.Контент"],
        operation_id="update one block content",
        request=ContentSerializer,
        responses={200: ContentSerializer},  # Ответ с обновленным объектом
    ),
    partial_update=extend_schema(
        summary="Частично обновить один блок Контента по его ID",
        tags=["Лендинг.Контент"],
        operation_id="partial update block content",
        request=ContentSerializer,
        responses={200: ContentSerializer},  # Ответ с частично обновленным объектом
    ),
    destroy=extend_schema(
        summary="Удалить один блок Контента по его ID",
        tags=["Лендинг.Контент"],
        operation_id="delete one block content",
        responses={204: None},  # Ответ с успешным удалением (нет содержимого)
    ),
)
class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    def get_permissions(self):
        """Переопределяем get_permissions, чтобы использовать разные права доступа для POST и GET"""
        permissions = [AllowAny] if self.request.method == "GET" else [IsSuperuserStaffAdmin]
        self.permission_classes = permissions
        return super().get_permissions()
