from rest_framework.pagination import PageNumberPagination


class BasePagination(PageNumberPagination):
    """
    Базовый класс для кастомной пагинации.
    """

    page_size = 20  # Количество объектов на одной странице
    # Максимальное количество объектов на странице, если используется page_size_query_param
    max_page_size = 50
    # Параметр, позволяющий пользователю задавать количество объектов на странице.
    page_size_query_param = "page_size"
    page_query_param = "page"  # Параметр для указания текущей страницы


def get_pagination_class(*args, **kwargs):
    """
    Фабрика для создания класса пагинации с заданными параметрами.
    """

    class CustomPagination(BasePagination):
        def __init__(self):
            for k, v in kwargs.items():
                setattr(self, k, v)

    return CustomPagination
