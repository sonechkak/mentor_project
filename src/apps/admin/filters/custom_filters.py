from datetime import timedelta, date

import django_filters
from django.db.models import Q


def is_not_value(func):
    def wrapper(self, qs, value, *args, **kwargs):
        if not value:
            return qs
        return func(self, qs, value, *args, **kwargs)

    return wrapper


class CustomEndDateFilter(django_filters.DateFilter):
    """Фильтр возвращает начало следующего дня что ровно конец текущего дня"""

    @is_not_value
    def filter(self, qs, value):
        if isinstance(value, date):
            if self.lookup_expr in ["lt", "lte"]:
                value += timedelta(days=1)

        return super().filter(qs, value)


class SearchFilter(django_filters.Filter):
    """Фильтрует по полям first_name и email"""

    @is_not_value
    def filter(self, qs, value):
        return qs.filter(Q(first_name__icontains=value) | Q(email__icontains=value))


class SearchArticleFilter(django_filters.Filter):
    """Фильтрует по полям title и content модели Article"""

    @is_not_value
    def filter(self, qs, value):
        return qs.filter(Q(title__icontains=value) | Q(content__icontains=value))
