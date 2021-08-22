import sqlite3
from datetime import datetime

import FinanceDataReader as fdr
import pandas as pd
from deprecated import deprecated
from pandas import DataFrame
from pykrx import stock

COL_TICKER = 'Symbol'
COL_CLOSE = 'Close'
COL_OPEN = 'Open'
COL_HIGH = 'High'
COL_LOW = 'Low'
COL_VOLUME = 'Volume'
COL_CHANGE = 'Change'
COL_DATE = 'Date'


def read_stock_list(market: str = None) -> DataFrame:
    """
    상장 종목 전체를 조회
    """
    if market is None:
        return read_stock_list_fdr()
    else:
        return read_stock_list_fdr(market)


def read_stock_list_fdr(market: str = 'KRX') -> DataFrame:
    """
    상장 종목 전체를 조회 [FinanceDataReader 이용]
    :param market: 마켓 구분 (KRX는 KOSPI,KOSDAQ,KONEX 모두 포함)
    """
    df = fdr.StockListing(market)  # KRX는 KOSPI,KOSDAQ,KONEX 모두 포함
    # print(df.head())
    return df


def read_prices_by_ticker(ticker: str, start_date: str, end_date: str = None) -> DataFrame:
    """
    한 종목의 가격 정보를 조회
    :param ticker: 종목코드
    :param start_date: 조회 시작일자 (yyyy-mm-dd)
    :param end_date: 조회 끝일자 (yyyy-mm-dd)
    :return: DataFrame
    """
    return read_prices_by_ticker_fdr(ticker, start_date, end_date)
    # return read_prices_by_ticker_pykrx(ticker, start_date, end_date)


def read_prices_by_ticker_fdr(ticker: str, start_date: str, end_date=None) -> DataFrame:
    """
    한 종목의 가격 정보를 조회 [FinanceDataReader 이용]
    :param ticker: 종목코드
    :param start_date: 조회 시작일자 (yyyy-mm-dd)
    :param end_date: 조회 끝일자 (yyyy-mm-dd)
    :return: DataFrame
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
    한 종목의 가격 정보를 조회 [PyKrx 이용]
    :param ticker: 종목코드
    :param start_date: 조회 시작일자 (yyyy-mm-dd)
    :param end_date: 조회 끝일자 (yyyy-mm-dd)
    :return: DataFrame
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


