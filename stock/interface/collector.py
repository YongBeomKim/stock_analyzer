import json
import time

from pandas import DataFrame, Series
from pandas._libs.tslibs.timestamps import Timestamp
from pykrx import stock
from datetime import datetime, timedelta


class StockItemCodeCollector:
    def __init__(self):
        self.markets = ['KOSPI', 'KOSDAQ', 'KONEX', 'ALL']
        self.tickers = dict()
        for market in self.markets:
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
    def convert_to_json(cls, df: DataFrame):
        json_list = list()
        for index in df.index:
            index: Timestamp
            index_per_date: str = index.strftime('%Y-%m-%d')
            series_per_date: Series = df.loc[index_per_date]
            json_str_per_date: str = series_per_date.to_json(force_ascii=False)
            json_per_date: dict = json.loads(json_str_per_date)
            json_per_date = cls.__convert_key_from_kor_to_eng_for_item(json_per_date)
            json_per_date['reg_date'] = index_per_date
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
        codes = list()
        code = code_collector.get_code(code_collector.markets[0], '삼성전자')
        codes.append(code)

        # 주식종목의 컬렉터 집합
        self.data_collectors = [StockItemDataFrameCollector(code) for code in codes]

    def process(self):
        while True:
            for data_collector in self.data_collectors:
                df = data_collector.get_dataframe_from_previous(10)
                json_data = Converter.convert_to_json(df)
                print(json_data)

            time.sleep(self.cycle)


if __name__ == '__main__':
    manager = Manager()
    manager.process()
