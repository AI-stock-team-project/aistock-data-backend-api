import sqlite3
import pandas as pd
from pandas import Series, DataFrame
import FinanceDataReader as fdr
from pykrx import stock
from deprecated import deprecated
from datetime import datetime, timedelta
import sqlalchemy
import os
import aistock.StockReader as StockReader
from aistock.StockReader import read_prices_by_dates
import aistock.database as aistock_database


class Table:
    __tablename__ = 'stock_price'
    code = 'code'
    symbol = 'code'
    date = 'date'
    open = 'open'
    high = 'high'
    low = 'low'
    close = 'close'
    volume = 'volume'
    trad_value = 'trad_value'
    fluc_rate = 'fluc_rate'


def get_engine():
    return aistock_database.connect()


def get_minmax_date() -> list:
    """
    테이블에 저장되어있는 주가데이터의 처음 날짜와 마지막 날짜를 조회
    """
    engine = get_engine()
    with engine.connect() as con:
        sql = f"""
            select 
                max({Table.date}) as max, 
                min({Table.date}) as min 
            from {Table.__tablename__}
            """
        rs = con.execute(sql)
        row = rs.fetchone()
        max_date = row['max'].strftime('%Y-%m-%d')
        min_date = row['min'].strftime('%Y-%m-%d')
    return [min_date, max_date]


def fetch_prices_by_dates(start_date: str, end_date: str):
    """
    특정 기간의 일정동안의 주가정보를 업데이트
    """
    print(start_date, end_date)
    df = read_prices_by_dates(start_date, end_date)

    print(df)

    # 원하는 컬럼만 지정... 일단 현재 기준으로 사용할 수 있는 건 다 사용하려고 함.
    df2 = df[[
        StockReader.COL_TICKER,
        StockReader.COL_DATE,
        StockReader.COL_OPEN,
        StockReader.COL_HIGH,
        StockReader.COL_LOW,
        StockReader.COL_CLOSE,
        StockReader.COL_VOLUME,
        StockReader.COL_TRAD_VALUE,
        StockReader.COL_FLUC_RATE
    ]]

    # 테이블에 이용할 컬럼명으로 변경
    df2.rename(columns={
        StockReader.COL_TICKER: Table.symbol,
        StockReader.COL_DATE: Table.date,
        StockReader.COL_OPEN: Table.open,
        StockReader.COL_HIGH: Table.high,
        StockReader.COL_LOW: Table.low,
        StockReader.COL_CLOSE: Table.close,
        StockReader.COL_VOLUME: Table.volume,
        StockReader.COL_TRAD_VALUE: Table.trad_value,
        StockReader.COL_FLUC_RATE: Table.fluc_rate
    }, inplace=True)

    df2[Table.fluc_rate] = df2[Table.fluc_rate].astype('str')
    # df2 = df2.drop(['trad_value', 'fluc_rate'], axis=1, inplace=True)
    # df2.index.name = 'id'

    df2.to_sql(Table.__tablename__, con=get_engine(), if_exists='append', index=False)


@deprecated
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
    df.to_sql(Table.__tablename__, con=get_engine(), if_exists='replace')


@deprecated
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
    df = pd.read_sql(f"select * from {Table.__tablename__} where {StockReader.COL_TICKER} = '{ticker}' and {StockReader.COL_DATE} >= datetime('{date}')",
                     con=get_engine(), parse_dates=[StockReader.COL_DATE])
    # df[COL_DATE] = pd.DatetimeIndex(df[COL_DATE])
    df.set_index(StockReader.COL_DATE, inplace=True)
    return df


def get_stock_close_price(symbol, date):
    df = pd.read_sql(f"select * from {Table.__tablename__} where Symbol = '{symbol}' and Date >= datetime('{date}')",
                     con=get_engine())
    # df.index = df['Date']()
    df['Date'] = pd.DatetimeIndex(df['Date'])
    df.set_index('Date', inplace=True)
    return df


@deprecated
def build_close_price_database(symbol, date):
    # symbol 과 date 를 기준으로 가장 최근의 날짜를 가져온다.
    # 그리고 그 이후 날짜의 값만 읽어와서 테이블에 넣는다.
    df = pd.read_sql(f"select max(Date) as max, min(Date) as min from {Table.__tablename__} where {StockReader.COL_TICKER} = '{symbol}' and Date >= datetime('{date}')",
                     con=get_engine())
    print(df)
    pass

