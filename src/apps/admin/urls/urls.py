from django.urls import path
from apps.admin.views import views

app_name = "admin"

urlpatterns = [
    path("list-users/", views.ListUsersView.as_view(), name="list_users"),
    path("edit/user/<int:id>/", views.EditUserView.as_view(), name="edit-user"),
    path("create/user/", views.CreateUserView.as_view(), name="create-user"),
]
