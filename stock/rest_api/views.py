from django.http import HttpResponse
from django.shortcuts import render

from rest_framework import viewsets 

from .serializers import StockUserSerializer, StockMarketSerializer, StockItemSerializer
from .models import StockUser, StockMarket, StockItem


# ModelViewSet URL
# DefaultRouter를 사용하여 해당 URL들이 자동으로 생성.

# rest_api/user/
# post_list = PostViewSet.as_view({
#     'get': 'list',
#     'post': 'create',
# })

# rest_api/user/{id}/
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


class StockItemViewSet(viewsets.ModelViewSet):
    queryset = StockItem.objects.all()
    serializer_class = StockItemSerializer
