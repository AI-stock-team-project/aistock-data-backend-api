import sqlite3
import pandas as pd
from pandas import Series, DataFrame
import FinanceDataReader as fdr
from pykrx import stock
from deprecated import deprecated
from datetime import datetime, timedelta
import sqlalchemy
import os
import StockReader
import aistock.database as aistock_database


table_name = 'stock_prices'


def get_engine():
    return aistock_database.connect_local()


def fetch_prices_by_ticker(ticker, date) -> None:
    """
    데이터를 읽어서 데이터베이스에 저장
    :param ticker: 
    :param date: 
    :return: None
    """
    df = StockReader.read_prices_by_ticker(ticker, date)
    # print(df)
    # print(type(df))
    df.to_sql(table_name, con=get_engine(), if_exists='replace')


def load():
    symbol = '095570'
    date = '2021-05-20'

    df = get_stock_close_price(symbol, date)
    print(type(df.index))
    print(df)


def retrieve_prices_by_ticker(ticker, date) -> DataFrame:
    """
    데이터베이스에서 해당되는 내역을 조회
    :param ticker:
    :type ticker: str
    :param date:
    :type date: str
    :return: DataFrame
    """
    df = pd.read_sql(f"select * from {table_name} where {StockReader.COL_TICKER} = '{ticker}' and {StockReader.COL_DATE} >= datetime('{date}')",
                     con=get_engine(), parse_dates=[StockReader.COL_DATE])
    # df[COL_DATE] = pd.DatetimeIndex(df[COL_DATE])
    df.set_index(StockReader.COL_DATE, inplace=True)
    return df


def get_stock_close_price(symbol, date):
    df = pd.read_sql(f"select * from {table_name} where Symbol = '{symbol}' and Date >= datetime('{date}')",
                     con=get_engine())
    # df.index = df['Date']()
    df['Date'] = pd.DatetimeIndex(df['Date'])
    df.set_index('Date', inplace=True)
    return df


def build_close_price_database(symbol, date):
    # symbol 과 date 를 기준으로 가장 최근의 날짜를 가져온다.
    # 그리고 그 이후 날짜의 값만 읽어와서 테이블에 넣는다.
    df = pd.read_sql(f"select max(Date) as max, min(Date) as min from {table_name} where {StockReader.COL_TICKER} = '{symbol}' and Date >= datetime('{date}')",
                     con=get_engine())
    print(df)
    pass
