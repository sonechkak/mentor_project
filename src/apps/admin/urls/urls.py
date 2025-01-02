from django.urls import path
from apps.admin.views import views

app_name = "admin"

urlpatterns = [
    path("list-users/", views.ListUsersView.as_view(), name="list_users"),
]
