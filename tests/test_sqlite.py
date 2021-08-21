from Class_Strategies import Strategies as st
from Class_Strategies import get_stocks
import pandas as pd
import FinanceDataReader as fdr
from pykrx import stock
from datetime import datetime, timedelta
# from sqlalchemy import create_engine
import StockSqlite


sqlite_file = '../CSV/test.db'
table_name = 'stock_price_close'


def test():
    """
    테스트 함수. 여기에 있는 내용을 테스트한다.
    :return: 
    """
    # test_build_close_price()
    test_get_stock_close_prices()


def test_build_close_price():
    StockSqlite.build_close_price_database('095570', '2021-01-01')


def test_insert_close_price_stock():
    """
    데이터베이스에 값을 넣는 경우
    :return: 
    """
    StockSqlite.load_stock_close_prices('095570', '2021-01-01')


def test_get_stock_close_prices():
    """

    :return:
    """
    symbol = '095570'
    date = '2021-05-20'

    df = StockSqlite.get_stock_close_price(symbol, date)
    print(type(df.index))
    print(df)


if __name__ == '__main__':
    test()
