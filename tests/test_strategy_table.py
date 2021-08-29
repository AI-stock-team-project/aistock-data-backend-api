"""
데이터베이스에서 전략별 종목 리스트를 조회,처리하는 기능에 대한 테스트
"""
import pandas as pd
from aistock.StockPrice import get_close_prices_by
from aistock.database import Base, db_session
import aistock.StrategyStock as StrategyStock


def test():
    """
    테스트 함수. 여기에 있는 내용을 테스트한다.
    """
    df = StrategyStock.retrieve_strategy_stocks('mo_1')
    print(df)


if __name__ == '__main__':
    test()
