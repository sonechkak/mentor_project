from django.urls import path

from apps.accounts.views import api_views

urlpatterns = [
    path("users/", api_views.UserRegistrationView.as_view(), name="user-register"),
]
