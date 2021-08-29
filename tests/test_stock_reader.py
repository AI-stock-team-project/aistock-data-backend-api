"""
외부 API를 이용해서, 주식 종목, 주가 데이터, 주가 인덱스 등을 조회하는 기능을 테스트
"""
import aistock.StockReader as StockReader


def test():
    df = StockReader.read_index_by('kospi', '2021-08-01', '2021-08-10')
    print(df)


if __name__ == '__main__':
    test()
