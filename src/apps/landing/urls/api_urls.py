from django.urls import path, include


from rest_framework import routers

from landing.views import api_views
from landing.views.api_views import *

router = routers.SimpleRouter()
router.register(r'aboutme', AboutMeViewSet)
router.register(r'content', ContentViewSet)

urlpatterns = [
    path("maininf", api_views.MainInfAPIViews.as_view(), name="main-inf-crud"),
    path('', include(router.urls)),
    #path("landing/main/<int:id>/", api_views.MainInfAPIView.as_view(), name="user-delete"),
]