"""
데이터베이스 테이블에 전략별 종목 리스트를 갱시하는 스크립트.

최초 1회 + 하루 한 번 정도로 호출되도록 설정한다.

entrypoint.sh 와 연관이 되므로, 파일명을 변경하지는 말 것.
"""
import pandas as pd
# noinspection PyUnresolvedReferences
from pandas import Series, DataFrame
# noinspection PyUnresolvedReferences
from datetime import timedelta, datetime, date
from aistock.StrategyStock import StrategyStockListTable, get_engine
import strategy.Strategies as st
import time


def update():
    """
    데이터베이스에 저장하는 함수
    """
    update_momentum_1month()


def update_momentum_1month():
    start = time.time()
    print("모멘텀 1 종목 리스트 만들기")

    df = st.momentum_1month()
    # print(df.iloc[:10])

    df = df[[
        'rank'
    ]]
    df.index.name = 'ticker'
    df.reset_index(drop=False, inplace=True)
    # df.rename(columns={
    #     'rank': 'rank'
    # })
    df['rank'] = df['rank'].astype('int')
    df.insert(0, 'strategy_code', 'mo_1')
    df.insert(len(df.columns), 'created_at', datetime.now())
    print(df.iloc[:10])
    # momentum_1mo_assets = df.index
    df.to_sql(
        name=StrategyStockListTable.__tablename__,
        con=get_engine(),
        if_exists='append',
        index=False
    )
    print(timedelta(seconds=(time.time() - start)))


def update_momentum_3month():
    start = time.time()
    print("모멘텀 1 종목 리스트 만들기")

    df = st.momentum_1month()
    # print(df.iloc[:10])

    df = df[[
        'rank'
    ]]
    df.index.name = 'ticker'
    df.reset_index(drop=False, inplace=True)
    # df.rename(columns={
    #     'rank': 'rank'
    # })
    df['rank'] = df['rank'].astype('int')
    df.insert(0, 'strategy_code', 'mo_1')
    df.insert(len(df.columns), 'created_at', datetime.now())
    print(df.iloc[:10])
    # momentum_1mo_assets = df.index
    df.to_sql(
        name=StrategyStockListTable.__tablename__,
        con=get_engine(),
        if_exists='append',
        index=False
    )
    print(timedelta(seconds=(time.time() - start)))


if __name__ == '__main__':
    update()
