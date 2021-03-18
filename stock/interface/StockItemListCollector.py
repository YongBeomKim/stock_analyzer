from datetime import datetime

from pykrx import stock

from StockMarketCollector import StockMarketCollector

from req_interface import CreateItemListReq
from req_interface import ReadItemListReq
from req_interface import UpdateItemListReq
from req_interface import DeleteItemListReq


class StockItemListCollector:
    def __init__(self):
        self.market_collector = StockMarketCollector()

    def get_whole_market_item_list_from_mongo(self):
        markets = self.market_collector.get_markets()
        for market in markets:
            market_name = market['stock_market_name']
            req = ReadItemListReq(market_name)
            res = req.send_get()
            yield {market_name: res.json()}

    def get_whole_market_item_list_from_pykrx(self):
        markets = self.market_collector.get_markets()
        today = datetime.today().strftime("%Y%m%d")
        for market in markets:
            market_name = market['stock_market_name']
            tickers = stock.get_market_ticker_list(today, market=market_name)
            yield {market_name: tickers}

    def post_item_list(self, tickers_in_market: dict):
        req = CreateItemListReq()
        for market_name in tickers_in_market.keys():
            tickers = tickers_in_market[market_name]
            for ticker in tickers:
                item_name = stock.get_market_ticker_name(ticker)
                params = {'stock_item_name': item_name,
                          'stock_item_code': ticker,
                          'stock_market_name': market_name}
                req.set_param(params)
                res = req.send_post()
                print(res.json())


c = StockItemListCollector()
for d in c.get_whole_market_item_list_from_pykrx():
    c.post_item_list(d)
