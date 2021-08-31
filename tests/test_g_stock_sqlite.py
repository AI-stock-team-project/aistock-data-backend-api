"""
데이터베이스에서 전략별 종목 리스트를 조회,처리하는 기능에 대한 테스트
"""
# noinspection PyUnresolvedReferences
import pandas as pd
import aistock.StockReader as StockReader
from sqlalchemy import create_engine
import os

# SQLITE 파일 경로
G_STOCKS_SQLITE = 'g_stocks.db'


def test():
    """
    테스트 함수. 여기에 있는 내용을 테스트한다.
    """
    # create_gstocks_sqlite()
    # s = retrieve_gstocks_sqlite()['ticker']
    # print(s.to_list())
    s = test_2()
    print(s)


def test_2():
    if os.path.exists(G_STOCKS_SQLITE):
        s = retrieve_gstocks_sqlite()['ticker']
        print('retrieve_gstocks_sqlite')
        return s.to_list()
    else:
        create_gstocks_sqlite()
        return StockReader.read_tickers_to_list()


def retrieve_gstocks_sqlite():
    df = pd.read_sql('g_stocks', con=get_gstocks_sqlite_engine())
    return df


def create_gstocks_sqlite():
    stocks = StockReader.read_tickers_to_list()
    df = pd.DataFrame(stocks, columns=["ticker"])
    df.to_sql('g_stocks', con=get_gstocks_sqlite_engine(), index=False, if_exists='replace')


def get_gstocks_sqlite_engine():
    engine = create_engine(f'sqlite:///{G_STOCKS_SQLITE}', echo=False)
    return engine


if __name__ == '__main__':
    test()
