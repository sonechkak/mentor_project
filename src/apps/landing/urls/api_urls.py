from django.urls import path, include
from rest_framework import routers

from apps.landing.views.api_views import *

router = routers.SimpleRouter()
router.register(r'aboutme', AboutMeViewSet)
router.register(r'content', ContentViewSet)
router.register(r'product', ProductViewSet)


urlpatterns = [
    path('maininf/', MainInfAPIViews.as_view({'get': 'list'}), name='maininf-list'),
    path('maininf/update/', MainInfAPIViews.as_view({'put': 'update'}), name='maininf-update'),
    path('maininf/partial-update/', MainInfAPIViews.as_view({'patch': 'partial_update'}),
         name='maininf-partial-update'),
    #path('maininf/delete/', MainInfAPIViews.as_view({'delete': 'destroy'}), name='maininf-delete'),
    path('', include(router.urls)),
    # path('product/', ProductAPIListView.as_view(), name='product-list'),
    # path('product/', ProductAPIListView.as_view(), name='product-list'),
]