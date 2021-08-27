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
    df1 = generate_momentum_1month()
    df2 = generate_momentum_3month()
    df3 = generate_speedy()
    df4 = generate_rising_date_freq()
    df5 = generate_dual_momentum()

    # 데이터 프레임 하나로 병합
    df = pd.concat([df1, df2, df3, df4, df5], ignore_index=True)
    # 작업일시를 추가
    df.insert(len(df.columns), 'created_at', datetime.now())
    print(df)
    df.to_sql(
        name=StrategyStockListTable.__tablename__,
        con=get_engine(),
        if_exists='append',
        index=False
    )


def generate_momentum_1month():
    """
    모멘텀 1개월 데이터 생성 및 테이블에 맞게 변환 후 반환

    :return:
        strategy_code  ticker  rank
    0          mo_1  247660     1
    1          mo_1  032280     2
    """
    strategy_code = 'mo_1'

    start = time.time()
    print("generate [momentum 1 months]")

    df = st.momentum_1month()
    df = df[[
        'rank'
    ]]
    df.index.name = 'ticker'
    df.reset_index(drop=False, inplace=True)
    # df.rename(columns={
    #     'rank': 'rank'
    # })
    df['rank'] = df['rank'].astype('int')
    df.insert(0, 'strategy_code', strategy_code)

    # 최대 200개까지만 추림
    df = df.iloc[:200]

    print(df.iloc[:10])
    print(timedelta(seconds=(time.time() - start)))

    return df


def generate_momentum_3month():
    """
    모멘텀 3개월 데이터 생성 및 테이블에 맞게 변환 후 반환

    :return:
        strategy_code  ticker  rank
    0          mo_1  247660     1
    1          mo_1  032280     2
    """
    strategy_code = 'mo_3'

    start = time.time()
    print("generate [momentum 3 months]")

    df = st.momentum_3months()
    df = df[[
        'rank'
    ]]
    df.index.name = 'ticker'
    df.reset_index(drop=False, inplace=True)
    # df.rename(columns={
    #     'rank': 'rank'
    # })
    df['rank'] = df['rank'].astype('int')
    df.insert(0, 'strategy_code', strategy_code)

    # 최대 200개까지만 추림
    df = df.iloc[:200]

    print(df.iloc[:10])
    print(timedelta(seconds=(time.time() - start)))

    return df


def generate_speedy():
    strategy_code = 'soaring'

    start = time.time()
    print("generate [soaring]")

    df = pd.DataFrame({'ticker': st.speedy_rising_volume()})
    df.insert(0, 'strategy_code', strategy_code)
    df.insert(len(df.columns), 'rank', 0)

    # 최대 200개까지만 추림
    df = df.iloc[:200]

    print(df.iloc[:10])
    print(timedelta(seconds=(time.time() - start)))

    return df


def generate_rising_date_freq():
    strategy_code = 'up_freq'

    start = time.time()
    print("generate [rising_date_freq]")

    df = st.get_up_down_zero_df()
    # up_freq 가 최소 0.01 이상되는 것만 추림.
    df = df[(df['up_freq'] > 0.01)]
    # print(df)
    df = df[[
        'stock',
        'up_rank'
    ]]
    df.rename(columns={
        'stock': 'ticker',
        'up_rank': 'rank'
    }, inplace=True)
    df['rank'] = df['rank'].astype('int')
    # df.drop(['up_rank'], axis=1, inplace=True)
    df.insert(0, 'strategy_code', strategy_code)

    # 최대 200개까지만 추림
    df = df.iloc[:200]

    # print(df)
    print(df.iloc[:10])
    print(timedelta(seconds=(time.time() - start)))

    return df


def generate_dual_momentum():
    strategy_code = 'dual_mo'

    start = time.time()
    print("generate [dual momentum]")

    df = pd.DataFrame({'ticker': st.get_dual_momentum_list()})
    df.insert(0, 'strategy_code', strategy_code)
    df.insert(len(df.columns), 'rank', 0)

    # 최대 200개까지만 추림
    df = df.iloc[:200]

    print(df.iloc[:10])
    print(timedelta(seconds=(time.time() - start)))

    return df


if __name__ == '__main__':
    update()
