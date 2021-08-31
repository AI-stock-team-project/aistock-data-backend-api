"""
pyKRX, FinanceDataReader등을 이용하여, 외부 통신 등으로 주식 종목, 주가 정보를 조회하는 기능들을 모아둔 모듈

함수 명칭 관련
- read_ticker_*** : 종목 코드만 반환하는 형태의 함수
- read_stock_*** : 종목의 상세 정보를 반환하는 형태의 함수
- read_prices_*** : 주가 정보를 반환하는 형태의 함수
"""
import datetime
import time
from datetime import timedelta
import FinanceDataReader as fdr
import pandas as pd
import numpy as np
from deprecated import deprecated
from pandas import DataFrame, json_normalize
from pykrx import stock
import requests
import json


# 종목 코드
COL_TICKER = 'Symbol'
# 기준 일자
COL_DATE = 'Date'
# 시가
COL_OPEN = 'Open'
# 고가
COL_HIGH = 'High'
# 저가
COL_LOW = 'Low'
# 종가
COL_CLOSE = 'Close'
# 거래량
COL_VOLUME = 'Volume'
# 거래대금
COL_TRAD_VALUE = 'Trad_value'
# 등락률
COL_FLUC_RATE = 'Fluc_rate'
COL_CHANGE = 'Fluc_rate'


class StockListCols:
    """
    종목 상세 목록을 불러올 때의 컬럼명
    read_stocklist_by_market 에서 이용
    """
    FULL_CODE = 'FullCode'
    CODE = 'Code'
    SYMBOL = 'Symbol'
    NAME = 'Name'
    MARKET = 'Market'
    MARKET_NAME = 'MarketName'
    MARKET_CODE = 'MarketCode'


def read_tickers_to_list() -> list:
    """
    종목을 조회하는 함수. pykrx를 통해서 로드함.
    :return: list 종목 코드 목록
    """
    return read_tickers_to_list_pykrx()


def read_tickers_to_list_pykrx() -> list:
    """
    종목을 조회하는 함수.
    'pykrx' 사용
    :return: list 종목 코드 목록
    """
    today = datetime.datetime.today().strftime("%Y%m%d")
    tickers = stock.get_market_ticker_list(today, market='KOSDAQ')
    tickers2 = stock.get_market_ticker_list(today, market='KOSPI')
    tickers.extend(tickers2)
    return list(tickers)


@deprecated
def read_tickers_to_list_pykrx_fundamental() -> list:
    """
    종목을 조회하는 함수. pykrx를 통해서 로드함.
    :return: 종목 코드 목록 (DataFrame)
    """
    today = datetime.datetime.today().strftime("%Y%m%d")
    kospi = stock.get_market_fundamental_by_ticker(today, market="KOSPI").index
    kosdaq = stock.get_market_fundamental_by_ticker(today, market="KOSDAQ").index
    tickers = kospi.append(kosdaq)
    # df_tickers = pd.DataFrame(tickers, columns=['ticker'])
    return list(tickers)


def read_stock_list() -> DataFrame:
    """
    라이브러리 없이 바로 주식 종목을 가져오는 기능 구현
    FinanceDataReader/krx/listing.py 을 참조해서 개선
    왠지 갯수가 안 맞는데? 갯수가 훨씬 많은 듯함.
    <사용>
    웹 서비스에서 초기에 주식 종목을 만들 때에 이용했음.
    실시간이라기보다는, 정보를 많이 갖고 있다는 것으로 보이므로, 초기 저장용도로 사용함.

    :return: 종목 목록 데이터프레임<br>
        FullCode	Code	Name	MarketCode	MarketName	Market	Symbol<br>
    0	KR7060310000	060310	3S	KSQ	코스닥	KOSDAQ	060310<br>
    1	KR7095570008	095570	AJ네트웍스	STK	유가증권	KOSPI	095570<br>
    2	KR7006840003	006840	AK홀딩스	STK	유가증권	KOSPI	006840
    """
    bld = 'dbms/comm/finder/finder_stkisu'
    r = requests.post('http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd', data={'bld': bld})
    jo = json.loads(r.text)
    """
    (KRX에서 로드된 데이터)
        full_code	short_code	codeName	marketCode	marketName	marketEngName	ord1	ord2
    0	KR7060310000	060310	3S	KSQ	코스닥	KOSDAQ		16
    1	KR7095570008	095570	AJ네트웍스	STK	유가증권	KOSPI		16
    2	KR7006840003	006840	AK홀딩스	STK	유가증권	KOSPI		16
    """
    df = json_normalize(jo, 'block1')
    df = df.rename(columns={
        'full_code': StockListCols.FULL_CODE,
        'short_code': StockListCols.CODE,
        'codeName': StockListCols.NAME,
        'marketCode': StockListCols.MARKET_CODE,
        'marketName': StockListCols.MARKET_NAME,
        'marketEngName': StockListCols.MARKET,
    })
    df[StockListCols.SYMBOL] = df[StockListCols.CODE]
    df.drop(['ord1', 'ord2'], inplace=True, axis=1)
    return df


@deprecated
def read_stock_list_fdr(market: str = 'KRX') -> DataFrame:
    """
    상장 종목 전체를 조회 [FinanceDataReader 이용]
    :param market: 마켓 구분 (KRX는 KOSPI,KOSDAQ,KONEX 모두 포함)
    """
    df = fdr.StockListing(market)  # KRX는 KOSPI,KOSDAQ,KONEX 모두 포함
    # print(df.head())
    return df


@deprecated
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


@deprecated
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


@deprecated
def read_prices_by_ticker_pykrx(ticker: str, start_date: str, end_date=None) -> DataFrame:
    """
    한 종목의 가격 정보를 조회
    [PyKrx 이용]
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
        today = datetime.datetime.today().strftime("%Y%m%d")
        df = stock.get_market_ohlcv_by_date(start_date, today, ticker)
    df.rename(
        columns={'시가': COL_OPEN, '고가': COL_HIGH, '저가': COL_LOW, '종가': COL_CLOSE, '거래량': COL_VOLUME},
        inplace=True)
    df.index.name = COL_DATE
    df.insert(0, COL_TICKER, ticker)
    return df


def read_prices_by_date(date) -> DataFrame:
    """
    특정 날짜의 전체 주식의 가격 정보 조회. (KOSPI/KOSDAQ/KONEX)
    [pykrx 이용]
    :param date: 기준 날짜 (yyyy-mm-dd)
    :return: DataFrame<br>
            Open	High	Low	Close	Volume	Trad_value	Fluc_rate<br>
    Symbol<br>
    060310	2915	2925	2850	2890	103210	297954910	-0.52<br>
    095570	5830	5940	5800	5920	44316	261164570	0.68<br>
    006840	35600	35900	34500	35400	69765	2460513500	-0.56<br>
    """
    print(f"read_prices_by_date ({date})")
    # df = pd.DataFrame()
    w_date = f'{date[:4]}{date[5:7]}{date[8:10]}'
    df = stock.get_market_ohlcv_by_ticker(w_date, 'ALL')
    col_map = {
        '시가': COL_OPEN,
        '고가': COL_HIGH,
        '저가': COL_LOW,
        '종가': COL_CLOSE,
        '거래량': COL_VOLUME,
        '거래대금': COL_TRAD_VALUE,
        '등락률': COL_FLUC_RATE
    }
    df.rename(
        columns=col_map,
        inplace=True)
    df.index.name = COL_TICKER
    # df.insert(0, COL_DATE, date)
    if df.iloc[0:15, 0].sum() > 0:
        # 값이 유효할 때 반환
        return df
    else:
        # 값이 0으로 채워진 경우는, 그냥 빈 DataFrame으로 반환
        return df[0:0]


def read_prices_by_dates(start_date: str, end_date: str) -> DataFrame:
    """
    특정 날짜부터 해당 날짜 까지의 전체 주식의 가격 정보를 조회.
    :param start_date: (yyyy-mm-dd)
    :param end_date: (yyyy-mm-dd)
    :return: DataFrame<br>
        Symbol	Date	Open	High	Low	Close	Volume	Trad_value	Fluc_rate<br>
    0	060310	2019-05-20	2605	2615	2470	2570	246378	626177635	-1.34<br>
    1	095570	2019-05-20	5570	5710	5320	5560	58514	322316850	-1.07<br>
    2	068400	2019-05-20	10750	10750	10350	10400	70136	738017450	-1.89
    """
    df = pd.DataFrame()
    days = (datetime.date.fromisoformat(end_date) - datetime.date.fromisoformat(start_date)).days + 1
    if days < 1:
        return pd.DataFrame()
    date = datetime.date.fromisoformat(start_date)
    for i in range(days):
        t_df = read_prices_by_date(date.strftime('%Y-%m-%d'))
        t_df.insert(0, COL_DATE, date)
        # print(t_df)
        # df.append(t_df)
        df = pd.concat([df, t_df])
        # 날짜를 +1 시킴
        date += timedelta(days=1)
        # 혹시 모르니까 sleep 추가
        time.sleep(1)
    df.reset_index(inplace=True)
    return df


def read_stop_stocks():
    """
    관리 종목을 조회하는 기능.
    (FinanceDataReader 이용)
    관리 종목은 관리받는 종목을 의미한다. 거래정지가 되어있거나 한다.
    """
    # KRX stock delisting symbol list and names 관리종목 리스트
    krx_adm = fdr.StockListing('KRX-ADMINISTRATIVE')  # 관리종목
    return krx_adm


def except_stop_stocks(tickers: list):
    # 거래 정지 목록을 조회
    stop_stocks = read_stop_stocks()['Symbol'].values
    # 거래 정지 목록을 제외한 나머지
    tickers_np = np.array(tickers)
    excepted_list = np.setdiff1d(tickers_np, stop_stocks)
    return excepted_list.tolist()


def read_index_by(index_symbol, start_date: str, end_date: str):
    """
    인덱스 주가를 가져오는 기능.
    (FinanceDataReader 이용)
    :param index_symbol: kospi/kosdaq
    :param start_date: 조회를 시작할 연월일 (yyyy-mm-dd)
    :param end_date: 조회를 마칠 연월일 (yyyy-mm-dd)
    """
    symbols = {
        'kospi': 'KS11',
        'kosdaq': 'KQ11'
    }
    index_symbol = index_symbol.lower()
    symbol = symbols[index_symbol]
    return fdr.DataReader(symbol, start_date, end_date)
