import sqlite3
import pandas as pd
from pandas import Series, DataFrame
import FinanceDataReader as fdr
from pykrx import stock
from deprecated import deprecated
from datetime import datetime, timedelta


sqlite_file = 'test2.db'
table_name = 'stock_prices'
COL_TICKER = 'Symbol'
COL_CLOSE = 'Close'
COL_OPEN = 'Open'
COL_HIGH = 'High'
COL_LOW = 'Low'
COL_VOLUME = 'Volume'
COL_CHANGE = 'Change'
COL_DATE = 'Date'


def build_close_price_database(symbol, date):
    # symbol 과 date 를 기준으로 가장 최근의 날짜를 가져온다.
    # 그리고 그 이후 날짜의 값만 읽어와서 테이블에 넣는다.
    engine = sqlite3.connect(sqlite_file)
    df = pd.read_sql(f"select max(Date) as max, min(Date) as min from {table_name} where {COL_TICKER} = '{symbol}' and Date >= datetime('{date}')", con=engine)
    print(df)
    pass


def read_prices_by_ticker(ticker: str, start_date: str, end_date: str = None) -> DataFrame:
    """
    통신으로 외부에서 stock_close_price를 읽어들임.
    :param ticker: 종목코드
    :param start_date: 조회 시작일자 (yyyy-mm-dd)
    :param end_date: 조회 끝일자 (yyyy-mm-dd)
    :return: DataFrame
    """
    return read_prices_by_ticker_fdr(ticker, start_date, end_date)
    # return read_prices_by_ticker_pykrx(ticker, start_date, end_date)


def read_prices_by_ticker_fdr(ticker: str, start_date: str, end_date=None) -> DataFrame:
    """
    FinanceDataReader를 이용하여 정보 조회
    :param ticker: 종목코드
    :param start_date: 조회 시작일자 (yyyy-mm-dd)
    :param end_date: 조회 끝일자 (yyyy-mm-dd)
    :return:
    """
    df = fdr.DataReader(ticker, start_date, end_date)
    df.rename(
        columns={'Open': COL_OPEN, 'High': COL_HIGH, 'Low': COL_LOW, 'Close': COL_CLOSE, 'Volume': COL_VOLUME,
                 'Change': COL_CHANGE},
        inplace=True)
    df.index.name = COL_DATE
    df.insert(0, COL_TICKER, ticker)
    return df


def read_prices_by_ticker_pykrx(ticker: str, start_date: str, end_date=None) -> DataFrame:
    """
    PyKrx를 이용하여 정보 조회
    :param ticker:
    :param start_date:
    :param end_date:
    :return:
    """
    start_date = f'{start_date[:4]}{start_date[5:7]}{start_date[8:10]}'
    if end_date is not None:
        end_date = f'{end_date[:4]}{end_date[5:7]}{end_date[8:10]}'

    if end_date is not None:
        df = stock.get_market_ohlcv_by_date(start_date, end_date, ticker)
    else:
        today = datetime.today().strftime("%Y%m%d")
        df = stock.get_market_ohlcv_by_date(start_date, today, ticker)
    df.rename(
        columns={'시가': COL_OPEN, '고가': COL_HIGH, '저가': COL_LOW, '종가': COL_CLOSE, '거래량': COL_VOLUME},
        inplace=True)
    df.index.name = COL_DATE
    df.insert(0, COL_TICKER, ticker)
    return df


@deprecated
def read_stock_close_prices(ticker='095570', date='2021-01-01'):
    """
    통신으로 외부에서 stock_close_price를 읽어들임.
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


def fetch_prices_by_ticker(ticker, date) -> None:
    """
    데이터를 읽어서 데이터베이스에 저장
    :param ticker: 
    :param date: 
    :return: None
    """
    engine = sqlite3.connect(sqlite_file)

    df = read_prices_by_ticker(ticker, date)
    # print(df)
    # print(type(df))
    df.to_sql(table_name, con=engine, if_exists='replace')


@deprecated
def fetch_stock_close_prices(symbol='095570', date='2021-01-01'):
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


def retrieve_prices_by_ticker(ticker, date) -> DataFrame:
    """
    데이터베이스에서 해당되는 내역을 조회
    :param ticker:
    :type ticker: str
    :param date:
    :type date: str
    :return: DataFrame
    """
    engine = sqlite3.connect(sqlite_file)
    df = pd.read_sql(f"select * from {table_name} where {COL_TICKER} = '{ticker}' and {COL_DATE} >= datetime('{date}')",
                     con=engine, parse_dates=[COL_DATE])
    # df[COL_DATE] = pd.DatetimeIndex(df[COL_DATE])
    df.set_index(COL_DATE, inplace=True)
    return df


def get_stock_close_price(symbol, date):
    engine = sqlite3.connect(sqlite_file)
    df = pd.read_sql(f"select * from {table_name} where Symbol = '{symbol}' and Date >= datetime('{date}')", con=engine)
    # df.index = df['Date']()
    df['Date'] = pd.DatetimeIndex(df['Date'])
    df.set_index('Date', inplace=True)
    return df

