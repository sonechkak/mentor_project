from django.urls import path

from apps.accounts.views import api_views

urlpatterns = [
    path("users/", api_views.UserCreateAndRetrieveListView.as_view(), name="user-create-and-list"),
]
