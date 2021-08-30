from sqlalchemy import create_engine
from sqlalchemy import BigInteger, Column, Integer, String, Float
import aistock.StockReader as StockReader

# SQLITE 파일 경로
SQLITE_PATH = 'stock_prices.db'


class StockPriceTable:
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


def get_engine():
    engine = create_engine(f'sqlite:///{SQLITE_PATH}', echo=True)
    return engine


def create_table() -> None:
    """
    SQLite에 테이블을 생성하는 함수
    """
    from sqlalchemy.orm import declarative_base
    # noinspection PyPep8Naming
    Base = declarative_base()

    class StockPrice(Base):
        """
        sqlalchemy 로 create 를 하기 위한 클래스
        """
        __tablename__ = StockPriceTable.__tablename__
        symbol = Column(StockPriceTable.symbol, String, primary_key=True)
        date = Column(StockPriceTable.date, String, primary_key=True)
        open = Column(StockPriceTable.open, Integer)
        high = Column(StockPriceTable.high, Integer)
        low = Column(StockPriceTable.low, Integer)
        close = Column(StockPriceTable.close, Integer)
        volume = Column(StockPriceTable.volume, Integer)
        trad_value = Column(StockPriceTable.trad_value, Integer)
        fluc_rate = Column(StockPriceTable.fluc_rate, String)

    StockPrice.__table__.create(bind=get_engine(), checkfirst=True)


def get_minmax_date() -> list:
    """
    테이블에 저장되어있는 주가데이터의 처음 날짜와 마지막 날짜를 조회
    """
    engine = get_engine()
    with engine.connect() as con:
        sql = f"""
            select 
                max({StockPriceTable.date}) as max, 
                min({StockPriceTable.date}) as min 
            from {StockPriceTable.__tablename__}
            """
        rs = con.execute(sql)
        row = rs.fetchone()
        max_date = row['max']
        min_date = row['min']
    return [min_date, max_date]


def fetch_prices_by_dates_sqlite(start_date: str, end_date: str):
    print(start_date, end_date)
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
        StockReader.COL_TICKER: StockPriceTable.symbol,
        StockReader.COL_DATE: StockPriceTable.date,
        StockReader.COL_OPEN: StockPriceTable.open,
        StockReader.COL_HIGH: StockPriceTable.high,
        StockReader.COL_LOW: StockPriceTable.low,
        StockReader.COL_CLOSE: StockPriceTable.close,
        StockReader.COL_VOLUME: StockPriceTable.volume,
        StockReader.COL_TRAD_VALUE: StockPriceTable.trad_value,
        StockReader.COL_FLUC_RATE: StockPriceTable.fluc_rate
    }, inplace=True)

    df2[StockPriceTable.fluc_rate] = df2[StockPriceTable.fluc_rate].astype('str')
    # df2 = df2.drop(['trad_value', 'fluc_rate'], axis=1, inplace=True)
    # df2.index.name = 'id'

    df2.to_sql(StockPriceTable.__tablename__, con=get_engine(), if_exists='append', index=False)
