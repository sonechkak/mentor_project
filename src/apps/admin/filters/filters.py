import django_filters
from django.contrib.auth import get_user_model

from apps.admin.filters.custom_filters import CustomEndDateFilter, SearchFilter, SearchArticleFilter
from apps.blog.models import Article


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


class SearchArticlesFilter(django_filters.FilterSet):
    search = SearchArticleFilter()
    comments_from = django_filters.NumberFilter(field_name="comments_qty", lookup_expr="gte")
    comments_to = django_filters.NumberFilter(field_name="comments_qty", lookup_expr="lte")
    views_from = django_filters.NumberFilter(field_name="views", lookup_expr="gte")
    views_to = django_filters.NumberFilter(field_name="views", lookup_expr="lte")
    likes_from = django_filters.NumberFilter(field_name="likes", lookup_expr="gte")
    likes_to = django_filters.NumberFilter(field_name="likes", lookup_expr="lte")
    dislikes_from = django_filters.NumberFilter(field_name="dislikes", lookup_expr="gte")
    dislikes_to = django_filters.NumberFilter(field_name="dislikes", lookup_expr="lte")

    class Meta:
        model = Article
        fields = []