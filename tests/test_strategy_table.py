"""
데이터베이스에서 전략별 종목 리스트를 조회,처리하는 기능에 대한 테스트
"""
# noinspection PyUnresolvedReferences
import pandas as pd
# noinspection PyUnresolvedReferences
from aistock.database import Base, db_session
import aistock.StrategyStock as StrategyStock


def test():
    """
    테스트 함수. 여기에 있는 내용을 테스트한다.
    """
    test_get_strategy_stocks_to_list()


def test_get_strategy_stocks_to_list():
    s = StrategyStock.get_strategy_stocks_to_list('mo_1')
    print(s)


if __name__ == '__main__':
    test()
