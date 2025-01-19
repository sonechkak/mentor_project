from django.urls import path

from apps.admin.views import api_views

urlpatterns = [
    path("generate-password/", api_views.GeneratePasswordView.as_view(), name="generate-password"),
]
