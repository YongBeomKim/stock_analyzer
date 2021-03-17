from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import StockUserViewSet
from .views import StockMarketViewSet
from .views import StockItemListViewSet
from .views import StockItemViewSet

router_user = DefaultRouter()
router_user.register('user', StockUserViewSet)

router_market = DefaultRouter()
router_market.register('market', StockMarketViewSet)

router_item_list = DefaultRouter()
router_item_list.register('item_list', StockItemListViewSet)

router_item = DefaultRouter()
router_item.register('item', StockItemViewSet)

urlpatterns = [
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('', include(router_user.urls)),
    path('', include(router_market.urls)),
    path('', include(router_item_list.urls)),
    path('', include(router_item.urls)),
]
