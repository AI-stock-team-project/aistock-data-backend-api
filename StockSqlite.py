import sqlite3
import pandas as pd
import FinanceDataReader as fdr
from pykrx import stock


sqlite_file = 'test.db'
table_name = 'stock_price_close'
COL_TICKER = 'Symbol'
COL_CLOSE = 'Close'


def build_close_price_database(symbol, date):
    # symbol 과 date 를 기준으로 가장 최근의 날짜를 가져온다.
    # 그리고 그 이후 날짜의 값만 읽어와서 테이블에 넣는다.
    engine = sqlite3.connect(sqlite_file)
    df = pd.read_sql(f"select max(Date) as max, min(Date) as min from {table_name} where {COL_TICKER} = '{symbol}' and Date >= datetime('{date}')", con=engine)
    print(df)
    pass


def read_stock_prices(ticker='095570', date='2021-01-01'):
    """
    통신으로 stock_close_price를 읽어들임.
    :param ticker:
    :param date:
    :return: DataFrame
    """
    df = pd.DataFrame()
    # ticker, date = '095570', '2021-08-01'
    # df['Close'] = fdr.DataReader(ticker, date)['Close']
    df[COL_CLOSE] = fdr.DataReader(ticker, date)['Close']
    df[COL_TICKER] = ticker
    return df


def read_stock_close_prices(ticker='095570', date='2021-01-01'):
    """
    통신으로 stock_close_price를 읽어들임.
    :param ticker: 
    :param date: 
    :return: DataFrame
    """
    df = pd.DataFrame()
    # ticker, date = '095570', '2021-08-01'
    # df['Close'] = fdr.DataReader(ticker, date)['Close']
    df[COL_CLOSE] = fdr.DataReader(ticker, date)['Close']
    df[COL_TICKER] = ticker
    return df


def load_stock_close_prices(symbol='095570', date='2021-01-01'):
    """
    해당하는 값을 통신으로 읽어서 sqlite에 저장
    :param symbol: 
    :param date: 
    :return: 
    """
    engine = sqlite3.connect(sqlite_file)

    df = read_stock_close_prices(symbol, date)
    # print(df)
    # print(type(df))
    df.to_sql(table_name, con=engine, if_exists='replace')


def load():
    symbol = '095570'
    date = '2021-05-20'

    df = get_stock_close_price(symbol, date)
    print(type(df.index))
    print(df)


def get_stock_close_price(symbol, date):
    engine = sqlite3.connect(sqlite_file)
    df = pd.read_sql(f"select * from {table_name} where Symbol = '{symbol}' and Date >= datetime('{date}')", con=engine)
    # df.index = df['Date']()
    df['Date'] = pd.DatetimeIndex(df['Date'])
    df.set_index('Date', inplace=True)
    return df

