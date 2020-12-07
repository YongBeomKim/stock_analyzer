from django.contrib import admin
from .models import StockUser, StockMarket, StockItem

# Register your models here.
admin.site.register(StockUser)
admin.site.register(StockMarket)
admin.site.register(StockItem)
