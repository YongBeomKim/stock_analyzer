from django.db import models


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

    def __str__(self):
        return self.stock_item_name
