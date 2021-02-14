from django.contrib import admin
from .models import StockUser
from .models import StockMarket
from .models import StockItem


# Register your models here.
@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ('stock_market', 'stock_item_name', 'reg_date', 'high', 'low', 'open', 'close', 'volume')
    list_display_links = ['stock_item_name']

# @admin.register(StockItem) 데코레이터로 대체
# admin.site.register(StockItem, StockItemAdmin)


admin.site.register(StockUser)
admin.site.register(StockMarket)
