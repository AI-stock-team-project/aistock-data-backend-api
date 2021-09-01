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
from aistock.StockPrice import StockPriceTable
import aistock.stock_prices_sqlite as stock_prices_sqlite
from aistock.stock_prices_sqlite import StockPriceSQLiteTable as StockPriceSQLiteTable
import time
from datetime import timedelta
from sqlalchemy import create_engine
import os


# FROM_TABLE = sqlite_table.StockPriceSqliteTable2
SQLITE_PATH = 'stock_prices.db'  # 기본값임. 변경 가능.


def get_engine():
    engine = create_engine(f'sqlite:///{SQLITE_PATH}', echo=True)
    return engine


def import_old_data():
    # 데이터베이스를 조회해서, row 가 없는 상태라면 sqlite 로 import 를 시행한다.
    if count_mysql_table() == 0:
        # 작업할 연도
        years = [
            '2016', '2017', '2018', '2019', '2020'
        ]
        global SQLITE_PATH
        back_sqlite_path = SQLITE_PATH
        for year in years:
            start = time.time()
            SQLITE_PATH = f'stock_prices_{year}.db'
            if not os.path.exists(SQLITE_PATH):
                print("[import_old_data] 파일이 없음. - " + SQLITE_PATH)
            else:
                import_from_sqlite()
            print(f"[import_stock_price] {year} [", timedelta(seconds=(time.time() - start)), ']')

        # 원래의 기본값으로 되돌려놓음
        SQLITE_PATH = back_sqlite_path
    else:
        print("[import_stock_price] 데이터가 있는 상태이므로 주가 정보 import를 진행하지 않음")


def load_from_sqlite() -> DataFrame:
    """
    sqlite 파일에서 읽어와서 mysql에 데이터를 넣는다.
    """
    df = pd.read_sql(f'select * from {StockPriceSQLiteTable.__tablename__}',
                     con=get_engine())
    return df


def import_from_sqlite():
    """
    stock_price 의 초기 데이터를 sqlite에서 읽어서 import 하는 함수.
    최초 1회에 실행된다.
    """
    df = load_from_sqlite()
    df.rename(
        columns={
            StockPriceSQLiteTable.symbol.name: StockPriceTable.symbol.name,
            StockPriceSQLiteTable.date.name: StockPriceTable.date.name,
            StockPriceSQLiteTable.open.name: StockPriceTable.open.name,
            StockPriceSQLiteTable.high.name: StockPriceTable.high.name,
            StockPriceSQLiteTable.low.name: StockPriceTable.low.name,
            StockPriceSQLiteTable.close.name: StockPriceTable.close.name,
            StockPriceSQLiteTable.volume.name: StockPriceTable.volume.name,
            StockPriceSQLiteTable.trad_value.name: StockPriceTable.trad_value.name,
            StockPriceSQLiteTable.fluc_rate.name: StockPriceTable.fluc_rate.name
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
        # 오래 전 데이터도 로드.
        import_old_data()
        # 최근 2021년 이후의 데이터 로드.
        import_from_sqlite()
        print("<< [import_stock_price] [", timedelta(seconds=(time.time() - main_start)), ']')
    else:
        print("[import_stock_price] 데이터가 있는 상태이므로 주가 정보 import를 진행하지 않음")
