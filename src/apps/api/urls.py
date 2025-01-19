from django.urls import path, include

from apps.accounts.urls.api_urls import urlpatterns as accounts_api_urls
from apps.admin.urls.api_urls import urlpatterns as admin_api_urls

app_name = "api"

urlpatterns = [
    path("v1/", include((accounts_api_urls, "accounts"), namespace="accounts-api")),
    path("v1/", include((admin_api_urls, "admin"), namespace="admin-api")),
]
