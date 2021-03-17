from django.http import HttpResponse
from django.shortcuts import render

from rest_framework import viewsets 

from .serializers import StockUserSerializer
from .serializers import StockMarketSerializer
from .serializers import StockItemListSerializer
from .serializers import StockItemSerializer


from .models import StockUser
from .models import StockMarket
from .models import StockItemList
from .models import StockItem


# ModelViewSet URL
# DefaultRouter를 사용하여 해당 URL들이 자동으로 생성.

# # rest_api/user/
# post_list = PostViewSet.as_view({
#     'get': 'list',
#     'post': 'create',
# })

# # rest_api/user/{id}/
# post_detail = PostViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy',
# })

# Create your views here.
class StockUserViewSet(viewsets.ModelViewSet):
    queryset = StockUser.objects.all()
    serializer_class = StockUserSerializer


class StockMarketViewSet(viewsets.ModelViewSet):
    queryset = StockMarket.objects.all()
    serializer_class = StockMarketSerializer


class StockItemListViewSet(viewsets.ModelViewSet):
    queryset = StockItemList.objects.all()
    serializer_class = StockItemListSerializer


class StockItemViewSet(viewsets.ModelViewSet):
    queryset = StockItem.objects.all()
    serializer_class = StockItemSerializer

    def get_queryset(self):
        # itemname = self.request.query_params.get('itemname', None)
        reg_date = self.request.query_params.get('reg_date', None)
        if reg_date is not None:
            # queryset = queryset.filter(stock_item_name=itemname)
            self.queryset = self.queryset.filter(reg_date=reg_date)
        return self.queryset
