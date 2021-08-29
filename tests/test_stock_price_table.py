"""
데이터베이스 테이블에서 가격 정보를 조회하는 기능에 대한 테스트
"""
# from CSV.Class_Strategies import Strategies as st
# from CSV.Class_Strategies import get_stocks
import pandas as pd
# from sqlalchemy import create_engine
# from aistock import StockPrice
from aistock.StockPrice import get_close_prices_by
from aistock.database import Base, db_session


def test():
    """
    테스트 함수. 여기에 있는 내용을 테스트한다.
    :return: 
    """
    # test_build_close_price()
    # test_fetch_stock_prices()
    # test_retrieve_prices_by_ticker()
    # test_get_close_prices_by()
    test_get_close_prices()


def test_get_close_prices():
    df = pd.DataFrame()
    stocklist = ['095570', '060310', '054620', '265520', '211270']
    for ticker in stocklist:
        df[ticker] = get_close_prices_by(ticker, begin_date='2021-08-19')['close']
    print(df)


def test_get_close_prices_by():
    df = get_close_prices_by('095570', begin_date='2021-08-19')
    # df = pd.read_sql(s.statement, db_session.bind)
    print(df)


if __name__ == '__main__':
    test()
