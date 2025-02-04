# schemas.py
from drf_spectacular.utils import extend_schema, OpenApiResponse
from landing.serializers.serializers import MainInfSerializer, AboutMeSerializer, ContentSerializer

# Общие константы
MAIN_INF_TAG = "Лендинг. Главная"
ABOUT_ME_TAG = "Лендинг: Обо Мне"
CONTENT_TAG = "Лендинг: Контент"

# Общие responses
MAIN_INF_RESPONSE = {200: MainInfSerializer}
ABOUT_ME_RESPONSE = {200: AboutMeSerializer(many=True)}
CONTENT_RESPONSE = {200: ContentSerializer(many=True)}

# Схемы для MainInfAPIViews
MAIN_INF_SCHEMAS = {
    "list": extend_schema(
        summary="Получить все данные из блока Главное",
        tags=[MAIN_INF_TAG],
        operation_id="get all main inf",
        responses=MAIN_INF_RESPONSE,
    ),
    "update": extend_schema(
        summary="Создать блок Главное (если его еще нет) или изменить все поля",
        tags=[MAIN_INF_TAG],
        operation_id="create or update all main inf",
        request=MainInfSerializer,
        responses=MAIN_INF_RESPONSE,
    ),
    "partial_update": extend_schema(
        summary="Изменить отдельные поля блока Главное",
        tags=[MAIN_INF_TAG],
        operation_id="partial update main inf",
        request=MainInfSerializer,
        responses=MAIN_INF_RESPONSE,
    ),
}

# Схемы для AboutMeViewSet
ABOUT_ME_SCHEMAS = {
    "list": extend_schema(
        summary="Получить список всех блоков Обо мне",
        tags=[ABOUT_ME_TAG],
        operation_id="get all about me",
        responses=ABOUT_ME_RESPONSE,
    ),
    "create": extend_schema(
        summary="Создать новый блок Обо мне",
        tags=[ABOUT_ME_TAG],
        operation_id="create new block about me",
        request=AboutMeSerializer,
        responses={201: AboutMeSerializer},
    ),
    "retrieve": extend_schema(
        summary="Получить блок Обо мне по его ID",
        tags=[ABOUT_ME_TAG],
        operation_id="get one block about me",
        request=AboutMeSerializer,
        responses={200: AboutMeSerializer},
    ),
    "update": extend_schema(
        summary="Обновить один блок Обо мне по его ID",
        tags=[ABOUT_ME_TAG],
        operation_id="update block about me",
        request=AboutMeSerializer,
        responses={200: AboutMeSerializer},
    ),
    "destroy": extend_schema(
        summary="Удалить один блок Обо мне по его ID",
        tags=[ABOUT_ME_TAG],
        operation_id="delete block about me",
        responses={204: None},
    ),
}

# Схемы для ContentViewSet
CONTENT_SCHEMAS = {
    "list": extend_schema(
        summary="Получить список всех блоков Контента",
        tags=[CONTENT_TAG],
        operation_id="get all contents",
        responses=CONTENT_RESPONSE,
    ),
    "create": extend_schema(
        summary="Создать новый блок Контента",
        tags=[CONTENT_TAG],
        operation_id="create new block content",
        request=ContentSerializer,
        responses={201: ContentSerializer},
    ),
    "retrieve": extend_schema(
        summary="Получить блок Контента по его ID",
        tags=[CONTENT_TAG],
        operation_id="get one block content",
        request=ContentSerializer,
        responses={200: ContentSerializer},
    ),
    "update": extend_schema(
        summary="Обновить один блок Контента по его ID",
        tags=[CONTENT_TAG],
        operation_id="update one block content",
        request=ContentSerializer,
        responses={200: ContentSerializer},
    ),
    "partial_update": extend_schema(
        summary="Частично обновить один блок Контента по его ID",
        tags=[CONTENT_TAG],
        operation_id="partial update block content",
        request=ContentSerializer,
        responses={200: ContentSerializer},
    ),
    "destroy": extend_schema(
        summary="Удалить один блок Контента по его ID",
        tags=[CONTENT_TAG],
        operation_id="delete one block content",
        responses={204: None},
    ),
}