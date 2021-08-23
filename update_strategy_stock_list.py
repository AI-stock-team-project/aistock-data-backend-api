"""
데이터베이스 테이블에 전략별 종목 리스트를 갱시하는 스크립트.

최초 1회 + 하루 한 번 정도로 호출되도록 설정한다.

entrypoint.sh 와 연관이 되므로, 파일명을 변경하지는 말 것.
"""
# noinspection PyPep8Naming
import aistock.database as aistock_database
import aistock.StockReader as StockReader

TABLE_STOCK_TEMP = 'stock_data_temp_2'


def update():
    """
    데이터베이스에 저장하는 함수
    """
    pass


if __name__ == '__main__':
    update()
