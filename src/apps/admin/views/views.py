from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth import get_user_model

from admin.forms.tag_form import TagEditForm
from blog.models import Tag, Category

from apps.admin.filters.filters import TagFilterSet
from apps.admin.forms.category_form import CategoryEditForm
from apps.core.decorators.decorators import log_request_operations
from apps.core.mixins.paginations.mixins import PaginationMixin
from apps.core.mixins.permissions.mixins import OnlyAdminAccessMixin
from apps.admin.filters import SearchUserFilter
from apps.admin.forms.user_forms import UserEditForm, UserCreateForm

User = get_user_model()


class ListUsersView(OnlyAdminAccessMixin, PaginationMixin, ListView):
    model = User
    template_name = "admin/list_users.html"
    ordering = ["id"]

    @log_request_operations(logger_name="admin")
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = SearchUserFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_users = super().get_queryset().count()
        context["total_users"] = total_users
        return context


class EditUserView(OnlyAdminAccessMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = "admin/edit_user.html"
    success_url = "/admin/list-users/"

    @log_request_operations(logger_name="admin")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @log_request_operations(logger_name="accounts")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.kwargs["id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context["date_joined"] = user.date_joined
        context["last_login"] = user.last_login
        context["avatar"] = user.avatar
        return context


class CreateUserView(OnlyAdminAccessMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "admin/create_user.html"
    success_url = "/admin/list-users/"

    @log_request_operations(logger_name="admin")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @log_request_operations(logger_name="accounts")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TagListView(OnlyAdminAccessMixin, PaginationMixin, ListView):
    model = Tag
    template_name = "admin/tags/list_tags.html"
    ordering = ["id"]

    @log_request_operations(logger_name="admin")
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = TagFilterSet(self.request.GET, queryset=queryset)
        return self.filter.qs


class TagEditView(OnlyAdminAccessMixin, UpdateView):
    model = Tag
    form_class = TagEditForm
    template_name = "admin/tags/tag_edit.html"
    success_url = reverse_lazy('admin:list_tags')

    @log_request_operations(logger_name="admin")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @log_request_operations(logger_name="admin")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        slug = self.kwargs["slug"]
        return get_object_or_404(Tag, slug=slug)


class TagCreateView(OnlyAdminAccessMixin, CreateView):
    model = Tag
    form_class = TagEditForm
    template_name = "admin/tags/tag_create.html"
    success_url = reverse_lazy('admin:list_tags')

    @log_request_operations(logger_name="admin")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @log_request_operations(logger_name="admin")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TagDeleteView(OnlyAdminAccessMixin, DeleteView):
    model = Tag
    template_name = "admin/tags/tag_confirm_delete.html"
    success_url = reverse_lazy('admin:list_tags')

    @log_request_operations(logger_name="admin")
    def get(self, request, *args, **kwargs):
        # Отображаем форму с подтверждением удаления
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        slug = self.kwargs["slug"]
        return get_object_or_404(Tag, slug=slug)