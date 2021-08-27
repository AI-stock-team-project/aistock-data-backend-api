"""
데이터베이스 테이블에 종목 리스트를 갱신하는 스크립트

최초 1회 + 하루 한 번 정도로 호출되도록 설정한다.

entrypoint.sh 와 연관이 되므로, 파일명을 변경하지는 말 것.
"""
# noinspection PyPep8Naming
import aistock.database as aistock_database
import aistock.StockReader as StockReader
from aistock.StockReader import StockListCols


class StockTable:
    table_name = 'stock'

    class Cols:
        code_isin = 'code_isin'
        code = 'code'
        symbol = 'symbol'
        name = 'name'
        market = 'market'


class StockTempTable:
    table_name = 'stock_list_temp'

    class Cols:
        code_isin = 'code_isin'
        code = 'code'
        symbol = 'symbol'
        name = 'name'
        market = 'market'


def update_stock_list():
    """
    종목 리스트를 데이터베이스에 저장 및 적용하는 기능
    """
    use_update = True

    # 디비 커넥션
    engine = aistock_database.connect()

    df = StockReader.read_stock_list()
    df = df.rename(columns={
        StockListCols.FULL_CODE: StockTempTable.Cols.code_isin,
        StockListCols.SYMBOL: StockTempTable.Cols.symbol,
        StockListCols.CODE: StockTempTable.Cols.code,
        StockListCols.NAME: StockTempTable.Cols.name,
        StockListCols.MARKET: StockTempTable.Cols.market
    })
    # 불필요한 컬럼 제거
    df.drop([StockListCols.MARKET_NAME], inplace=True, axis=1)

    # 데이터 임시 테이블 생성 (테이블이 있을 경우 지우고 새로 작성)
    df.to_sql(con=engine, name=StockTempTable.table_name, if_exists='replace')

    if use_update:
        # 실제 테이블로 옮기기 위한 작업
        with engine.connect() as connection:
            # 임시 테이블과 비교해서 기존에 없던 신규 내용을 insert

            query_insert_new = f"""
                insert into {StockTable.table_name}(
                    {StockTable.Cols.code}, {StockTable.Cols.code_isin}, {StockTable.Cols.symbol},
                    {StockTable.Cols.name}, {StockTable.Cols.market}, 
                    is_active
                ) select 
                    {StockTempTable.Cols.code}, {StockTempTable.Cols.code_isin}, {StockTempTable.Cols.symbol},
                    {StockTempTable.Cols.name}, {StockTempTable.Cols.market},
                    1 as is_active
                from {StockTempTable.table_name}
                where {StockTempTable.Cols.symbol} not in (select {StockTable.Cols.symbol} from {StockTable.table_name})
                """

            # 기존에 있었는데 변경사항을 update
            # noinspection PyUnusedLocal
            query_update_exists = f"""
                update {StockTable.table_name} as a
                inner join {StockTempTable.table_name} as b
                on a.{StockTable.Cols.symbol} = b.{StockTempTable.Cols.symbol}
                set 
                    a.{StockTable.Cols.name} = b.{StockTempTable.Cols.name},
                    a.{StockTable.Cols.code_isin} = b.{StockTempTable.Cols.code_isin},
                    a.{StockTable.Cols.market} = b.{StockTempTable.Cols.market}
                """

            # 이전에 있었으나 더이상 사용되지 않는 경우는 is_active 를 0으로 변경
            query_removed_data = f"""
                update {StockTable.table_name}
                set is_active = 0
                where {StockTable.Cols.symbol} not in (select {StockTempTable.Cols.symbol} from {StockTempTable.table_name})
                """

            # 기존의 테이블에 값을 처리
            # connection.execute(query_update_exists)
            connection.execute(query_insert_new)
            connection.execute(query_removed_data)


if __name__ == '__main__':
    update_stock_list()
