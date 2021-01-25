from django.db import models
from django.utils import timezone


# Create your models here.
class StockUser(models.Model):
    user_name = models.CharField(max_length=200)
    # bookmark_item_list = models.CharField(max_length=200) # 연구중..

    def __str__(self):
        return self.user_name


class StockMarket(models.Model):
    stock_market_name = models.CharField(max_length=200)

    def __str__(self):
        return self.stock_market_name


class StockItem(models.Model):
    stock_market = models.ForeignKey(StockMarket, on_delete=models.CASCADE)
    stock_item_name = models.CharField(max_length=200)
    reg_date = models.DateTimeField(default=timezone.now(), null=True)
    # high = models.FloatField(default=0.0000)
    # low = models.FloatField(default=0.0000)
    # open = models.FloatField(default=0.0000)
    # close = models.FloatField(default=0.0000)
    # volume = models.FloatField(default=0.0000)
    # adj_close = models.FloatField(default=0.0000)

    def __str__(self):
        return self.stock_item_name
