import time
import pandas as pd
import pandas_datareader as pdr

from pandas import DataFrame

# 2021.01.05.hsk : 병렬처리 연구 필요
# from multiprocessing import Process


class StockItemCodeCollector:
    keys = ['회사명', '종목코드']

    def __init__(self):
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download'
        self.df: DataFrame = pd.read_html(url, header=0)[0]
        self.df = self.df[self.keys]
        self.hash_table = self.convert_to_hashable(self.df)

    @classmethod
    def convert_to_hashable(cls, df: DataFrame):
        """
        2021.02.04.hsk : 회사명과 종목코드를 자기고 있는 DataFrame을 딕셔너리(hashable) 형태로 반환
        """
        hash_table = dict()
        for index, row in df.iterrows():
            key = row[cls.keys[0]]
            val = row[cls.keys[1]]
            hash_table[key] = val
        return hash_table

    def get_code(self, company_name):
        return self.hash_table[company_name]


class StockItemCollector:
    def __init__(self, item):
        self.item = item
        self.table = None

    def collect(self):
        print('[{0}]'.format(self.item))
        self.table = pdr.get_data_yahoo(self.item)
        print(self.table)


if __name__ == '__main__':
    code_collector = StockItemCodeCollector()
    code = code_collector.get_code('삼성전자')

    ks_code = '{:06d}.KS'.format(code)  # 코스피 코드
    kq_code = '{:06d}.KQ'.format(code)  # 코스닥 코드
    stock_items = [ks_code, kq_code]
    # 업데이트 주기
    cycle = 10
    # 주식종목의 컬렉터 집합
    collectors = [StockItemCollector(stock_item) for stock_item in stock_items]

    while True:
        print(collectors)
        for collector in collectors:
            collector.collect()
        time.sleep(cycle)
