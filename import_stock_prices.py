"""
[SQLite에서 주가 정보를 읽어서 테이블에 넣는 스크립트]
- 미리 만들어놓은 주가 정보를 sqlite로부터 읽어서 테이블에 넣는다.
- 최초 1회에만 실행되는 스크립트.

[동작설명]
1. mysql 테이블에 row가 있는지 살핀다. row가 있으면 진행하지 않는다.
2. 1건도 데이터가 없을 때, sqlite에서 데이터를 로드해서 insert를 해준다.
"""
# noinspection PyPep8Naming
import aistock.database as aistock_database
import pandas as pd
from pandas import DataFrame
from aistock import stock_prices_sqlite as sqlite_table
from aistock.StockPrice import StockPriceTable
import time
from datetime import timedelta


FROM_TABLE = sqlite_table.StockPriceTable


def load_from_sqlite() -> DataFrame:
    """
    sqlite 파일에서 읽어와서 mysql에 데이터를 넣는다.
    """
    df = pd.read_sql(f'select * from {FROM_TABLE.__tablename__}',
                     con=sqlite_table.get_engine())
    return df


def import_from_sqlite():
    """
    stock_price 의 초기 데이터를 sqlite에서 읽어서 import 하는 함수.
    최초 1회에 실행된다.
    """
    df = load_from_sqlite()
    df.rename(
        columns={
            FROM_TABLE.symbol: StockPriceTable.symbol.name,
            FROM_TABLE.date: StockPriceTable.date.name,
            FROM_TABLE.open: StockPriceTable.open.name,
            FROM_TABLE.high: StockPriceTable.high.name,
            FROM_TABLE.low: StockPriceTable.low.name,
            FROM_TABLE.close: StockPriceTable.close.name,
            FROM_TABLE.volume: StockPriceTable.volume.name,
            FROM_TABLE.trad_value: StockPriceTable.trad_value.name,
            FROM_TABLE.fluc_rate: StockPriceTable.fluc_rate.name
        },
        inplace=True
    )
    df[StockPriceTable.fluc_rate.name] = df[StockPriceTable.fluc_rate.name].astype('str')
    # print(df.dtypes)

    df.to_sql(
        StockPriceTable.__tablename__,
        con=aistock_database.connect(),
        if_exists='append',
        index=False,
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
            from {StockPriceTable.__tablename__}
            """
        rs = con.execute(sql)
        row = rs.fetchone()
        count = row['count']
    return count


if __name__ == '__main__':
    # 데이터베이스를 조회해서, row 가 없는 상태라면 sqlite 로 import 를 시행한다.
    if count_mysql_table() == 0:
        main_start = time.time()
        print("[import_stock_price] >> ")
        import_from_sqlite()
        print("<< [import_stock_price] [", timedelta(seconds=(time.time() - main_start)), ']')
    else:
        print("[import_stock_price] 데이터가 있는 상태이므로 주가 정보 import를 진행하지 않음")
