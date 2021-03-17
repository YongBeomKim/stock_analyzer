from req_interface import CreateMarketReq
from req_interface import ReadMarketReq
from req_interface import UpdateMarketReq
from req_interface import DeleteMarketReq

class StockMarketCollector:
    def get_markets(self):
        req = ReadMarketReq()
        res = req.send_get()
        return res.json()

