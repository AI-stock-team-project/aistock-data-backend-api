"""
SQLite 주가 테이블 파일을 생성하기 위한 기능들을 담고 있는 모듈
테이블명, 컬럼명을 이용하는 데에 사용된다. (import_stock_prices.py 에서 이용됨)
(SQLite 파일 생성은 가급적 CoLab에서 진행한다. 아이피 차단을 회피할 수 있기 때문)
"""
from sqlalchemy import create_engine
# noinspection PyUnresolvedReferences
from sqlalchemy import BigInteger, Column, Integer, String
import aistock.StockReader as StockReader
from sqlalchemy.orm import declarative_base

# SQLITE 파일 경로
SQLITE_PATH = 'stock_prices.db'

# noinspection PyPep8Naming
Base = declarative_base()


class StockPriceSQLiteTable(Base):
    """
    sqlalchemy 로 create 를 하기 위한 클래스
    """
    __tablename__ = 'stock_price_temp'
    # 종목 코드
    symbol = Column('symbol', String, primary_key=True)
    # 기준 일자
    date = Column('date', String, primary_key=True)
    # 시가
    open = Column('open', Integer)
    # 고가
    high = Column('high', Integer)
    # 저가
    low = Column('low', Integer)
    # 종가
    close = Column('close', Integer)
    # 거래량
    volume = Column('volume', Integer)
    # 거래대금
    trad_value = Column('trad_value', Integer)
    # 등락률
    fluc_rate = Column('fluc_rate', String)


"""
class StockPriceSqliteTable2:
    __tablename__ = 'stock_price_temp'
    symbol = 'symbol'
    date = 'date'
    open = 'open'
    high = 'high'
    low = 'low'
    close = 'close'
    volume = 'volume'
    trad_value = 'trad_value'
    fluc_rate = 'fluc_rate'
"""


def get_engine():
    engine = create_engine(f'sqlite:///{SQLITE_PATH}', echo=True)
    return engine


def create_table() -> None:
    """
    SQLite에 테이블을 생성하는 함수
    """
    StockPriceSQLiteTable.__table__.create(bind=get_engine(), checkfirst=True)


def get_minmax_date() -> list:
    """
    테이블에 저장되어있는 주가데이터의 처음 날짜와 마지막 날짜를 조회
    """
    engine = get_engine()
    with engine.connect() as con:
        sql = f"""
            select 
                max({StockPriceSQLiteTable.date.name}) as max, 
                min({StockPriceSQLiteTable.date.name}) as min 
            from {StockPriceSQLiteTable.__tablename__}
            """
        rs = con.execute(sql)
        row = rs.fetchone()
        max_date = row['max']
        min_date = row['min']
    return [min_date, max_date]


def fetch_prices_by_dates_sqlite(start_date: str, end_date: str):
    """
    테이블에 로드한 데이터를 반영
    """
    print(f"fetch_prices_by_dates_sqlite {start_date} {end_date}")
    df = StockReader.read_prices_by_dates(start_date, end_date)

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
        StockReader.COL_TICKER: StockPriceSQLiteTable.symbol.name,
        StockReader.COL_DATE: StockPriceSQLiteTable.date.name,
        StockReader.COL_OPEN: StockPriceSQLiteTable.open.name,
        StockReader.COL_HIGH: StockPriceSQLiteTable.high.name,
        StockReader.COL_LOW: StockPriceSQLiteTable.low.name,
        StockReader.COL_CLOSE: StockPriceSQLiteTable.close.name,
        StockReader.COL_VOLUME: StockPriceSQLiteTable.volume.name,
        StockReader.COL_TRAD_VALUE: StockPriceSQLiteTable.trad_value.name,
        StockReader.COL_FLUC_RATE: StockPriceSQLiteTable.fluc_rate.name
    }, inplace=True)

    df2[StockPriceSQLiteTable.fluc_rate.name] = df2[StockPriceSQLiteTable.fluc_rate.name].astype('str')
    # df2 = df2.drop(['trad_value', 'fluc_rate'], axis=1, inplace=True)
    # df2.index.name = 'id'

    df2.to_sql(StockPriceSQLiteTable.__tablename__, con=get_engine(), if_exists='append', index=False)
