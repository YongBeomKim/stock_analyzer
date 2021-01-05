from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import StockItemCollector
from .views import StockUserViewSet, StockMarketViewSet, StockItemViewSet

router_user = DefaultRouter()
router_user.register('user', StockUserViewSet)

router_market = DefaultRouter()
router_market.register('market', StockMarketViewSet)

router_item = DefaultRouter()
router_item.register('item', StockItemViewSet)

urlpatterns = [
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('', include(router_user.urls)),
    path('', include(router_market.urls)),
    path('', include(router_item.urls)),
]
