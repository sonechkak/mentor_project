from django.urls import path, include


from rest_framework import routers

from landing.views import api_views
from landing.views.api_views import *

router = routers.SimpleRouter()
router.register(r'aboutme', AboutMeViewSet)
router.register(r'content', ContentViewSet)


urlpatterns = [
    path('maininf/', MainInfAPIViews.as_view({'get': 'list'}), name='maininf-list'),
    path('maininf/update/', MainInfAPIViews.as_view({'put': 'update'}), name='maininf-update'),
    path('maininf/partial-update/', MainInfAPIViews.as_view({'patch': 'partial_update'}),
         name='maininf-partial-update'),
    #path('maininf/delete/', MainInfAPIViews.as_view({'delete': 'destroy'}), name='maininf-delete'),
    path('', include(router.urls)),
]