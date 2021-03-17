from rest_framework import serializers
from django.contrib.auth.models import User

from .models import StockUser
from .models import StockMarket
from .models import StockItemList
from .models import StockItem



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class StockUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockUser
        fields = '__all__'


class StockMarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMarket
        fields = '__all__'


class StockItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockItemList
        fields = '__all__'


class StockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockItem
        fields = '__all__'
