import time
import pandas_datareader as pdr

# 2021.01.05.hsk : 병렬처리 연구 필요
# from multiprocessing import Process

class StockItemCollector:
    def __init__(self, item):
        self.item = item

    def collect(self):
        print('[{0}]'.format(self.item))
        table = pdr.get_data_yahoo(self.item)
        print(table)

if __name__ == '__main__':
    # 주식시장 목록, 이 부분도 대체 필요 (하드코딩 x)
    stock_items = ['067160.KQ', 'msft']
    # 업데이트 주기
    cycle = 10
    # 주식종목의 컬렉터 집합
    collectors = list()
    
    # processes = list()

    for stock_item in stock_items:
        collector = StockItemCollector(stock_item)
        collectors.append(collector)

    while True:
        for collector in collectors:
            collector.collect()
        time.sleep(cycle)
