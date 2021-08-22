# from CSV.Class_Strategies import Strategies as st
# from CSV.Class_Strategies import get_stocks
# import pandas as pd
# from sqlalchemy import create_engine
from aistock import StockReader


def test():
    """
    테스트 함수. 여기에 있는 내용을 테스트한다.
    :return: 
    """
    # test_build_close_price()
    # test_fetch_stock_prices()
    test_retrieve_prices_by_ticker()


def test_fetch_stock_prices():
    StockReader.fetch_prices_by_ticker('095570', '2021-08-01')


def test_build_close_price():
    StockReader.build_close_price_database('095570', '2021-01-01')


def test_retrieve_prices_by_ticker():
    df = StockReader.retrieve_prices_by_ticker('095570', '2021-01-01')
    # print(type(df.index))
    print(df)


def test_get_stock_prices():
    pass


def test_get_stock_close_prices():
    """

    :return:
    """
    symbol = '095570'
    date = '2021-05-20'

    df = StockReader.get_stock_close_price(symbol, date)
    print(type(df.index))
    print(df)


if __name__ == '__main__':
    test()
