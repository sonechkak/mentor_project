from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.contrib.auth import get_user_model

from apps.core.decorators.decorators import log_request_operations
from apps.core.mixins.paginations.mixins import PaginationMixin
from apps.core.mixins.permissions.mixins import OnlyAdminAccessMixin
from apps.admin.filters import SearchUserFilter
from apps.admin.forms import UserEditForm

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
