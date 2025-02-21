from django.contrib.auth import get_user_model

import django_filters

from .custom_filters import CustomEndDateFilter, SearchFilter, SearchTagFilter
from blog.models import Tag


class SearchUserFilter(django_filters.FilterSet):
    search = SearchFilter()
    date_joined_from = django_filters.DateTimeFilter(field_name="date_joined", lookup_expr="gte")
    date_joined_to = CustomEndDateFilter(field_name="date_joined", lookup_expr="lte")
    last_login_from = django_filters.DateTimeFilter(field_name="last_login", lookup_expr="gte")
    last_login_to = CustomEndDateFilter(field_name="last_login", lookup_expr="lte")
    is_active = django_filters.BooleanFilter(field_name="is_active", lookup_expr="exact")

    class Meta:
        model = get_user_model()
        fields = ["is_active"]

class TagFilterSet(django_filters.FilterSet):
    search = SearchTagFilter(field_name="tag_name", lookup_expr="icontains")  # Поиск по вхождению

    class Meta:
        model = Tag
        fields = []  # Оставляем пустым, так как 'search' не является полем модели