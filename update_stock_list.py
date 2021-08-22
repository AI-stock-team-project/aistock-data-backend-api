# noinspection PyPep8Naming
import aistock.database as aistock_database
import aistock.StockReader as StockReader

TABLE_STOCK_TEMP = 'stock_data_temp'


def get_stock_list():
    """
    종목 정보 가져오기
    """
    # 한국거래소 상장종목 전체
    return StockReader.read_stock_list('KRX')


def update_stock_list():
    """
    종목 리스트를 데이터베이스에 저장하는 함수
    """
    df = get_stock_list()

    engine = aistock_database.get_engine()

    # 데이터 임시 테이블 생성 (테이블이 있을 경우 지우고 새로 작성)
    df.to_sql(con=engine, name=TABLE_STOCK_TEMP, if_exists='replace')

    # 실제 테이블로 옮기기 위한 작업
    with engine.connect() as connection:
        # 임시 테이블과 비교해서 기존에 없던 신규 내용을 insert
        query_insert_new = f"""
            insert into stock(
                code, symbol,
                name, market, sector, industry, 
                listing_date, settle_month, representative, homepage, 
                is_active
            ) select 
                Symbol, Symbol,
                Name, Market, Sector, Industry, 
                date(ListingDate), SettleMonth, Representative, HomePage,
                1 as is_active
            from {TABLE_STOCK_TEMP}
            where Symbol not in (select symbol from stock)
            """

        # 기존에 있었는데 변경사항을 update
        # noinspection PyUnusedLocal
        query_update_exists = f"""
            update stock as a
            inner join {TABLE_STOCK_TEMP} as b
            on a.symbol = b.Symbol
            set 
                a.name = b.Name 
                ,a.market = b.Market 
                ,a.sector = b.Sector 
                ,a.industry = b.Industry
                ,a.listing_date = date(b.ListingDate) 
                ,a.settle_month = b.SettleMonth 
                ,a.representative = b.Representative 
                ,a.homepage =  b.HomePage
            """
        
        # 이전에 있었으나 더이상 사용되지 않는 경우는 is_active 를 0으로 변경
        query_removed_data = f"""
            update stock
            set is_active = 0
            where symbol not in (select Symbol from {TABLE_STOCK_TEMP})
            """

        # 기존의 테이블에 값을 처리
        # connection.execute(query_update_exists)
        connection.execute(query_insert_new)
        connection.execute(query_removed_data)


if __name__ == '__main__':
    update_stock_list()
