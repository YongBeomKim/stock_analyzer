import time

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
                print(df.head(3))
            time.sleep(self.cycle)


if __name__ == '__main__':
    manager = Manager()
    manager.process()

# class StockItemCodeCollector:
#     keys = ['회사명', '종목코드']
#
#     def __init__(self):
#         url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download'
#         self.df: DataFrame = pd.read_html(url, header=0)[0]
#         self.df = self.df[self.keys]
#         self.hash_table = self.convert_to_hashable(self.df)
#
#     @classmethod
#     def convert_to_hashable(cls, df: DataFrame):
#         """
#         2021.02.04.hsk : 회사명과 종목코드를 자기고 있는 DataFrame을 딕셔너리(hashable) 형태로 반환
#         """
#         hash_table = dict()
#         for index, row in df.iterrows():
#             key = row[cls.keys[0]]
#             val = row[cls.keys[1]]
#             hash_table[key] = val
#         return hash_table
#
#     def get_code(self, company_name):
#         return self.hash_table[company_name]


# class StockItemCollector:
#     def __init__(self, item):
#         self.item = item
#         self.table = None
#
#     def collect(self):
#         print('[{0}]'.format(self.item))
#         self.table = pdr.get_data_yahoo(self.item)
#         print(self.table)
