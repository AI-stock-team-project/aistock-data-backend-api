# noinspection PyUnresolvedReferences
from datetime import timedelta, datetime

import pandas as pd
# noinspection PyUnresolvedReferences
from deprecated import deprecated
from pandas import DataFrame
from sqlalchemy import Column, Integer, String, select

import aistock.StockReader as StockReader
import aistock.database as aistock_database
from aistock.StockReader import read_prices_by_dates
from aistock.database import Base, db_session


class StockPriceTable(Base):
    """
    sqlalchemy의 ORM 을 이용하기 위한 모델
    """
    __tablename__ = 'stock_price'
    id = Column('id', String, primary_key=True)
    symbol = Column('code', String)
    date = Column('date', String)
    open = Column('open', Integer)
    high = Column('high', Integer)
    low = Column('low', Integer)
    close = Column('close', Integer)
    volume = Column('volume', Integer)
    trad_value = Column('trad_value', Integer)
    fluc_rate = Column('fluc_rate', String)

    def __repr__(self):
        return f"{self.id} {self.symbol} {self.date} {self.open} {self.high} {self.low} {self.close} {self.volume} {self.trad_value} {self.fluc_rate}"


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
                max({str(StockPriceTable.date.name)}) as max, 
                min({str(StockPriceTable.date.name)}) as min 
            from {StockPriceTable.__tablename__}
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
        StockReader.COL_TICKER: StockPriceTable.symbol.name,
        StockReader.COL_DATE: StockPriceTable.date.name,
        StockReader.COL_OPEN: StockPriceTable.open.name,
        StockReader.COL_HIGH: StockPriceTable.high.name,
        StockReader.COL_LOW: StockPriceTable.low.name,
        StockReader.COL_CLOSE: StockPriceTable.close.name,
        StockReader.COL_VOLUME: StockPriceTable.volume.name,
        StockReader.COL_TRAD_VALUE: StockPriceTable.trad_value.name,
        StockReader.COL_FLUC_RATE: StockPriceTable.fluc_rate.name
    }, inplace=True)

    df2[StockPriceTable.fluc_rate.name] = df2[StockPriceTable.fluc_rate.name].astype('str')
    # df2 = df2.drop(['trad_value', 'fluc_rate'], axis=1, inplace=True)
    # df2.index.name = 'id'

    df2.to_sql(StockPriceTable.__tablename__, con=get_engine(), if_exists='append', index=False)


def get_prices_by(ticker, date=None, begin_date=None, end_date=None) -> DataFrame:
    """
    get_prices_by(ticker) : 오늘(또는 마지막) 날짜의 주가 정보
    get_prices_by(ticker, date='yyyy-mm-dd') : 특정 날짜의 주가 정보
    get_prices_by(ticker, begin_date='yyyy-mm-dd') : 특정 날짜부터 최근 날짜까지의 주가 정보
    get_prices_by(ticker, begin_date='yyyy-mm-dd', end_date='yyyy-mm-dd') : 두 날짜 사이에 해당하는 주가 정보
    """
    return retrieve_prices_by(ticker, date, begin_date, end_date)


def get_close_prices_by(ticker, date=None, begin_date=None, end_date=None) -> DataFrame:
    """
    get_close_prices_by(ticker) : 오늘(또는 마지막) 날짜의 종가
    get_close_prices_by(ticker, date='yyyy-mm-dd') : 특정 날짜의 종가
    get_close_prices_by(ticker, begin_date='yyyy-mm-dd') : 특정 날짜부터 최근 날짜까지의 종가
    get_close_prices_by(ticker, begin_date='yyyy-mm-dd', end_date='yyyy-mm-dd') : 두 날짜 사이에 해당하는 종가
    """
    if ticker is None:
        raise

    select_stmt = select(StockPriceTable.date, StockPriceTable.symbol, StockPriceTable.close)
    return retrieve_prices_by(ticker, date, begin_date, end_date, select_stmt=select_stmt)


def get_volumes_by(ticker, date=None, begin_date=None, end_date=None) -> DataFrame:
    """
    get_close_prices_by(ticker) : 오늘(또는 마지막) 날짜의 거래량
    get_close_prices_by(ticker, date='yyyy-mm-dd') : 특정 날짜의 거래량
    get_close_prices_by(ticker, begin_date='yyyy-mm-dd') : 특정 날짜부터 최근 날짜까지의 거래량
    get_close_prices_by(ticker, begin_date='yyyy-mm-dd', end_date='yyyy-mm-dd') : 두 날짜 사이에 해당하는 거래량
    """
    if ticker is None:
        raise

    select_stmt = select(StockPriceTable.date, StockPriceTable.symbol, StockPriceTable.volume)
    return retrieve_prices_by(ticker, date, begin_date, end_date, select_stmt=select_stmt)


def retrieve_prices_by(ticker, date=None, begin_date=None, end_date=None, select_stmt=None) -> DataFrame:
    """
    retrieve_prices_by(ticker) : 오늘(또는 마지막) 날짜의 주가 정보
    retrieve_prices_by(ticker, date='yyyy-mm-dd') : 특정 날짜의 주가 정보
    retrieve_prices_by(ticker, begin_date='yyyy-mm-dd') : 특정 날짜부터 최근 날짜까지의 주가 정보
    retrieve_prices_by(ticker, begin_date='yyyy-mm-dd', end_date='yyyy-mm-dd') : 두 날짜 사이에 해당하는 주가 정보

    retrieve_prices_by(ticker, select_stmt) : 특정 컬럼만 조회할 때
    """
    if ticker is None:
        raise

    if select_stmt is None:
        # 특정 select 영역이 없으면 전체 컬럼 조회
        select_stmt = select(StockPriceTable)
    
    if date is not None:
        # 해당 컬럼만 조회
        stmt = select_stmt.where(
            StockPriceTable.symbol == ticker,
            StockPriceTable.date == date
        )
        df = pd.read_sql(stmt, db_session.bind)
        df.set_index(StockPriceTable.date.name, inplace=True)
        return df

    if begin_date is not None:
        if end_date is None:
            # 최근 날짜로 end_date 셋팅
            end_date = datetime.today().strftime("%Y-%m-%d")

        # 구간에 대한 조회
        stmt = select_stmt.where(
            StockPriceTable.symbol == ticker,
            StockPriceTable.date.between(begin_date, end_date)
        ).order_by(StockPriceTable.date.asc())
        df = pd.read_sql(
            stmt,
            db_session.bind,
            parse_dates=[StockPriceTable.date.name]
        )
        df.set_index(StockPriceTable.date.name, inplace=True)
        return df
    raise
