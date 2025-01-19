from django.urls import path

from apps.accounts.views import api_views

urlpatterns = [
    path("users/", api_views.UserListCreateView.as_view(), name="user-create-and-list"),
    path("users/<int:id>/", api_views.UserDeleteView.as_view(), name="user-delete"),
    path(
        "users/<int:id>/change-password/",
        api_views.UserChangePasswordView.as_view(),
        name="change-password",
    ),
]
