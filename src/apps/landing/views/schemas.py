from drf_spectacular.utils import extend_schema

from apps.landing.serializers.serializers import (
    MainInfSerializer,
    AboutMeSerializer,
    ContentSerializer,
    ProductSerializer,
)

# Общие константы
MAIN_INF_TAG = "Лендинг: Главная"
ABOUT_ME_TAG = "Лендинг: Обо Мне"
CONTENT_TAG = "Лендинг: Контент"
PRODUCTS_TAG = "Лендинг: Продукты"

# Общие responses
MAIN_INF_RESPONSE = {200: MainInfSerializer}
ABOUT_ME_RESPONSE = {200: AboutMeSerializer(many=True)}
CONTENT_RESPONSE = {200: ContentSerializer(many=True)}
PRODUCTS_RESPONSE = {200: ProductSerializer(many=True)}
CREATE_RESPONSE = {201: None}
UPDATE_RESPONSE = {200: None}
DELETE_RESPONSE = {204: None}

# Схемы для MainInfAPIViews
MAIN_INF_SCHEMAS = {
    "list": extend_schema(
        summary="Получить все данные из блока Главное",
        description="Этот эндпоинт возвращает полный список всех данных из блока 'Главное'.",
        tags=[MAIN_INF_TAG],
        operation_id="get_all_main_inf",
        responses=MAIN_INF_RESPONSE,
    ),
    "update": extend_schema(
        summary="Создать блок Главное (если его еще нет) или изменить все поля",
        description="Позволяет создать блок 'Главное' (если его ещё нет) или изменить все его поля.",
        tags=[MAIN_INF_TAG],
        operation_id="create_or_update_all_main_inf",
        request=MainInfSerializer,
        responses=MAIN_INF_RESPONSE,
    ),
    "partial_update": extend_schema(
        summary="Изменить отдельные поля блока Главное",
        description="Позволяет изменить отдельные поля блока 'Главное'.",
        tags=[MAIN_INF_TAG],
        operation_id="partial_update_main_inf",
        request=MainInfSerializer,
        responses=MAIN_INF_RESPONSE,
    ),
}

# Схемы для AboutMeViewSet
ABOUT_ME_SCHEMAS = {
    "list": extend_schema(
        summary="Получить список всех блоков Обо мне",
        description="Этот эндпоинт возвращает полный список всех блоков 'Обо мне'.",
        tags=[ABOUT_ME_TAG],
        operation_id="get_all_about_me",
        responses=ABOUT_ME_RESPONSE,
    ),
    "create": extend_schema(
        summary="Создать новый блок Обо мне",
        description="Позволяет создать новый блок 'Обо мне' с указанными параметрами.",
        tags=[ABOUT_ME_TAG],
        operation_id="create_new_block_about_me",
        request=AboutMeSerializer,
        responses=CREATE_RESPONSE,
    ),
    "retrieve": extend_schema(
        summary="Получить блок Обо мне по его ID",
        description="Возвращает подробное представление блока 'Обо мне' по указанному идентификатору.",
        tags=[ABOUT_ME_TAG],
        operation_id="get_one_block_about_me",
        responses={200: AboutMeSerializer},
    ),
    "update": extend_schema(
        summary="Обновить один блок Обо мне по его ID",
        description="Позволяет полностью обновить блок 'Обо мне' по его идентификатору.",
        tags=[ABOUT_ME_TAG],
        operation_id="update_block_about_me",
        request=AboutMeSerializer,
        responses=UPDATE_RESPONSE,
    ),
    "destroy": extend_schema(
        summary="Удалить один блок Обо мне по его ID",
        description="Удаляет блок 'Обо мне' по указанному идентификатору.",
        tags=[ABOUT_ME_TAG],
        operation_id="delete_block_about_me",
        responses=DELETE_RESPONSE,
    ),
}

# Схемы для ContentViewSet
CONTENT_SCHEMAS = {
    "list": extend_schema(
        summary="Получить список всех блоков Контента",
        description="Этот эндпоинт возвращает полный список всех блоков контента.",
        tags=[CONTENT_TAG],
        operation_id="get_all_contents",
        responses=CONTENT_RESPONSE,
    ),
    "create": extend_schema(
        summary="Создать новый блок Контента",
        description="Позволяет создать новый блок контента с указанными параметрами.",
        tags=[CONTENT_TAG],
        operation_id="create_new_block_content",
        request=ContentSerializer,
        responses=CREATE_RESPONSE,
    ),
    "retrieve": extend_schema(
        summary="Получить блок Контента по его ID",
        description="Возвращает подробное представление блока контента по указанному идентификатору.",
        tags=[CONTENT_TAG],
        operation_id="get_one_block_content",
        responses={200: ContentSerializer},
    ),
    "update": extend_schema(
        summary="Обновить один блок Контента по его ID",
        description="Позволяет полностью обновить блок контента по его идентификатору.",
        tags=[CONTENT_TAG],
        operation_id="update_one_block_content",
        request=ContentSerializer,
        responses=UPDATE_RESPONSE,
    ),
    "partial_update": extend_schema(
        summary="Частично обновить один блок Контента по его ID",
        description="Позволяет частично обновить блок контента по его идентификатору.",
        tags=[CONTENT_TAG],
        operation_id="partial_update_block_content",
        request=ContentSerializer,
        responses=UPDATE_RESPONSE,
    ),
    "destroy": extend_schema(
        summary="Удалить один блок Контента по его ID",
        description="Удаляет блок контента по указанному идентификатору.",
        tags=[CONTENT_TAG],
        operation_id="delete_one_block_content",
        responses=DELETE_RESPONSE,
    ),
}

# Схемы для ProductViewSet
PRODUCT_SCHEMAS = {
    "list": extend_schema(
        summary="Получить список всех продуктов",
        description="Этот эндпоинт возвращает полный список всех существующих продуктов.",
        tags=[PRODUCTS_TAG],
        operation_id="get_all_products",
        responses=PRODUCTS_RESPONSE,
    ),
    "create": extend_schema(
        summary="Создать новый продукт",
        description="Позволяет создать новый продукт с указанными параметрами. В продукте должно быть от 1 до 7 пунктов.",
        tags=[PRODUCTS_TAG],
        operation_id="create_product",
        request=ProductSerializer,
        responses=CREATE_RESPONSE,
    ),
    "retrieve": extend_schema(
        summary="Получить информацию о конкретном продукте",
        description="Возвращает подробную информацию о продукте по указанному идентификатору.",
        tags=[PRODUCTS_TAG],
        operation_id="get_product_by_id",
        responses={200: ProductSerializer},
    ),
    "update": extend_schema(
        summary="Полностью обновить продукт",
        description="Позволяет полностью обновить информацию о продукте по его идентификатору. В продукте должно быть от 1 до 7 пунктов.",
        tags=[PRODUCTS_TAG],
        operation_id="update_product",
        request=ProductSerializer,
        responses=UPDATE_RESPONSE,
    ),
    "partial_update": extend_schema(
        summary="Частично обновить продукт",
        description="Позволяет частично обновить информацию о продукте по его идентификатору. В продукте должно быть от 1 до 7 пунктов.",
        tags=[PRODUCTS_TAG],
        operation_id="partial_update_product",
        request=ProductSerializer,
        responses=UPDATE_RESPONSE,
    ),
    "destroy": extend_schema(
        summary="Удалить продукт",
        description="Удаляет продукт по указанному идентификатору.",
        tags=[PRODUCTS_TAG],
        operation_id="delete_product",
        responses=DELETE_RESPONSE,
    ),
}