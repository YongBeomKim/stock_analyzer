from django.http import HttpResponse
from django.shortcuts import render

from rest_framework import viewsets

from .serializers import StockUserSerializer, StockMarketSerializer, StockItemSerializer
from .models import StockUser, StockMarket, StockItem


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
