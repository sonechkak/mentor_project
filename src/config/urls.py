from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", include("admin.urls.urls", namespace="admin")),
    path("accounts/", include("accounts.urls.urls", namespace="accounts")),
    path("blog/", include("blog.urls", namespace="blog")),
    path("", include("landing.urls.urls", namespace="landing")),
    path("api/", include("api.urls", namespace="api")),
    re_path("", include("social_django.urls", namespace="social")),
    # DRF Spectacular : OpenAPI 3.0
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI
    path(
        "schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
    # ReDoc
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
