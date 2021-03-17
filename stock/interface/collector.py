import json
import time

from pykrx import stock
from pandas import DataFrame, Series
from datetime import datetime, timedelta

from interface.req_interface import ReadMarketReq
from interface.req_interface import ReadItemListReq
from interface.req_interface import ReadItemReq

from interface.req_interface import CreateMarketReq
from interface.req_interface import CreateItemListReq
from interface.req_interface import CreateItemReq


class StockItemListCollector:
    def __init__(self):
        self.stock = stock

    def save_market_code_name(self, date, market):
        item_codes = stock.get_market_ticker_list(date, market=market)
        for item_code in item_codes:
            item_name = stock.get_market_ticker_name(item_code)
            item_code = int(item_code)
            data = {
                        "stock_item_name": item_name,
                        "stock_item_code": item_code,
                        "stock_market_name": market
                    }
            req = CreateItemListReq()
            req.set_param(data)


class StockItemCodeCollector:
    def __init__(self):
        # self.markets = ['KOSPI', 'KOSDAQ', 'KONEX', 'ALL']
        self.markets = {'KOSPI': 1, 'KOSDAQ': 2, 'KONEX': 3, 'ALL': 4}
        self.tickers = dict()
        for market in self.markets.keys():
            self.tickers[market] = self.__collect_tickers(market)

    @staticmethod
    def __collect_tickers(market='KOSPI'):
        """
        stock.get_market_ticker_list()
        >> ['095570', '006840', '027410', '282330', '138930', ...]

        stock.get_market_ticker_name(ticker)
        >> SK하이닉스
        """
        tickers = dict()
        today = datetime.today().strftime("%Y%m%d")

        for ticker in stock.get_market_ticker_list(today, market):
            ticker_name = stock.get_market_ticker_name(ticker)
            tickers[ticker_name] = ticker
        return tickers

    def get_code(self, market, ticker_name):
        return self.tickers[market][ticker_name]


class StockItemDataFrameCollector:
    def __init__(self, code):
        self.code = code
        self.today = datetime.now()
        self.today_str = self.today.strftime("%Y%m%d")

    def get_dataframe_from_previous(self, days=1):
        interval = timedelta(days)
        previous = self.today - interval
        previous_str = previous.strftime("%Y%m%d")
        dataframe = stock.get_market_ohlcv_by_date(previous_str, self.today_str, self.code)
        return dataframe


class Converter:
    @classmethod
    def convert_to_json_for_item(cls, df: DataFrame, market: int, company: str):
        json_list = list()
        for index in df.index:
            # 각 날짜별 행을 딕셔너리로 가져오는 과정
            index_per_date: str = index.strftime('%Y-%m-%d')  # index: TimeStamp
            series_per_date: Series = df.loc[index_per_date]
            json_str_per_date: str = series_per_date.to_json(force_ascii=False)
            json_per_date: dict = json.loads(json_str_per_date)

            # 주식시장, 종목, 등록일 삽입
            json_per_date['stock_market'] = market
            json_per_date['stock_item_name'] = company
            json_per_date['reg_date'] = index_per_date

            # 한글로 된 키를 영문으로 변경
            json_per_date = cls.__convert_key_from_kor_to_eng_for_item(json_per_date)

            json_list.append(json_per_date)
        return json_list

    @staticmethod
    def __convert_key_from_kor_to_eng_for_item(json_per_date: dict):
        replacements = {'시가': 'open',
                        '종가': 'close',
                        '고가': 'high',
                        '저가': 'low',
                        '거래량': 'volume'}

        for key_kor, key_eng in replacements.items():
            json_per_date[key_eng] = json_per_date.pop(key_kor)

        return json_per_date


class Manager:
    def __init__(self):
        # 업데이트 주기
        self.cycle = 10

        code_collector = StockItemCodeCollector()
        dict_market = code_collector.markets
        list_market = list(dict_market.keys())

        self.market = list_market[0]  # KOSPI
        self.market_id = dict_market[self.market]
        self.company = '삼성전자'

        code = code_collector.get_code(self.market, self.company)
        codes = list()
        codes.append(code)

        # 주식종목의 컬렉터 집합
        self.data_collectors = [StockItemDataFrameCollector(code) for code in codes]

    def process(self):
        while True:
            for data_collector in self.data_collectors:
                df = data_collector.get_dataframe_from_previous(10)
                json_data = Converter.convert_to_json_for_item(df, self.market_id, self.company)
                # print(json_data)
                req = CreateItemReq()
                req.set_param(json_data)
                res = req.send_post()

            time.sleep(self.cycle)


if __name__ == '__main__':
    manager = Manager()
    manager.process()
