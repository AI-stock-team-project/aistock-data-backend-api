"""
"""
# noinspection PyPep8Naming
import aistock.database as aistock_database
import aistock.StockReader as StockReader
from aistock.StockReader import StockKrxCols
import aistock.dateutil as aistock_dateutil
import pandas as pd
from pandas import Series, DataFrame
import stock_prices_sqlite as sqlite_table
import aistock.StockPriceTable as StockPriceTable
from sqlalchemy import Float, Integer, DateTime, String


FROM_TABLE = sqlite_table.StockPriceTable
TO_TABLE = StockPriceTable.Table


def load_from_sqlite() -> DataFrame:
    """
    sqlite 파일에서 읽어와서 mysql에 데이터를 넣는다.
    """
    df = pd.read_sql(f'select * from {FROM_TABLE.__tablename__}',
                     con=sqlite_table.get_engine())
    return df


def import_from_sqlite():
    df = load_from_sqlite()
    df.rename(
        columns={
            FROM_TABLE.symbol: TO_TABLE.code,
            FROM_TABLE.date: TO_TABLE.date,
            FROM_TABLE.open: TO_TABLE.open,
            FROM_TABLE.high: TO_TABLE.high,
            FROM_TABLE.low: TO_TABLE.low,
            FROM_TABLE.close: TO_TABLE.close,
            FROM_TABLE.volume: TO_TABLE.volume,
            FROM_TABLE.trad_value: TO_TABLE.trad_value,
            FROM_TABLE.fluc_rate: TO_TABLE.fluc_rate
        },
        inplace=True
    )
    print(df.dtypes)

    df.to_sql(
        TO_TABLE.__tablename__,
        con=aistock_database.connect(),
        if_exists='append',
        index=False,
        dtype={TO_TABLE.fluc_rate: Float}
    )


def count_mysql_table() -> int:
    """
    주가 정보 테이블의 데이터 갯수를 조회
    """
    engine = aistock_database.connect()
    with engine.connect() as con:
        sql = f"""
            select 
                count(*) as count
            from {TO_TABLE.__tablename__}
            """
        rs = con.execute(sql)
        row = rs.fetchone()
        count = row['count']
    return count


if __name__ == '__main__':
    # 데이터베이스를 조회해서, row 가 없는 상태라면 sqlite 로 import 를 시행한다.
    if count_mysql_table() == 0:
        import_from_sqlite()
    else:
        print("[import_stock_price] 데이터가 있는 상태이므로 주가 정보 import를 진행하지 않음")
