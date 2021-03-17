from pykrx import stock

from StockMarketCollector import StockMarketCollector

from req_interface import CreateItemListReq
from req_interface import ReadItemListReq
from req_interface import UpdateItemListReq
from req_interface import DeleteItemListReq

class StockItemListCollector:
    def __init__(self):
        self.market_collector = StockMarketCollector()

    def get_item_list(self):
        markets = self.market_collector.get_markets()
        for market in markets:
            print(market)
        idx = int(input('select index : '))
        selected_market = markets[idx]
        req = ReadItemListReq(selected_market['stock_market_name'])
        res = req.send_get()
        return res.json()

    def post_item_list(self):
        pass

