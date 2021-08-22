# noinspection PyPep8Naming
import FinanceDataReader as fdr
import sqlalchemy
import os
import sys


# 데이터를 가져오기
def get_data():
    # 한국거래소 상장종목 전체
    df_krx = fdr.StockListing('KRX')  # KRX는 KOSPI,KOSDAQ,KONEX 모두 포함
    # print(df_krx.head())
    return df_krx


def update_stock_list():
    # 데이터를 DB에 넣기
    df = get_data()

    database_host = os.getenv('DB_HOST', 'localhost')
    database_port = os.getenv('DB_PORT', '3306')
    database_name = os.getenv('DB_DATABASE', 'default')
    database_username = os.getenv('DB_USER', 'default')
    database_password = os.getenv('DB_PASSWORD', '')
    engine = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}'.
                                      format(database_username, database_password,
                                             database_host, database_port, database_name))

    # 데이터 임시 테이블 생성
    df.to_sql(con=engine, name='stock_data_temp', if_exists='replace')

    # 실제 테이블로 옮기기 위한 작업
    with engine.connect() as con:
        # 임시 테이블과 비교해서 기존에 없던 신규 내용을 insert
        query_insert_new = """
            insert into stock(
              code, code_isin, symbol,
                name, market, sector, industry, 
                listing_date, settle_month, representative, homepage, 
                is_active
            ) select 
              Symbol, FullCode, Symbol,
                Name, Market, Sector, Industry, 
              date(ListingDate), SettleMonth, Representative, HomePage,
              1 as is_active
            from stock_data_temp
            where Symbol not in (select symbol from stock)
            """

        # 기존에 있었는데 변경사항을 update
        query_update_exists = """
            update stock as a
            inner join stock_data_temp as b
            on a.symbol = b.Symbol
            set 
               a.code_isin = b.FullCode
                ,a.name = b.Name 
                ,a.market = b.Market 
                ,a.sector = b.Sector 
                ,a.industry = b.Industry
                ,a.listing_date = date(b.ListingDate) 
                ,a.settle_month = b.SettleMonth 
                ,a.representative = b.Representative 
                ,a.homepage =  b.HomePage
            """
        query_removed_data = """
            update stock
            set is_active = 0
            where symbol not in (select Symbol from stock_data_temp)
            """

        # 기존의 테이블에 값을 처리
        con.execute(query_insert_new)
        con.execute(query_removed_data)
        con.execute(query_update_exists)


if __name__ == '__main__':
    update_stock_list()
