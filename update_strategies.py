"""
데이터베이스 테이블에 전략별 종목 리스트를 갱시하는 스크립트.

최초 1회 + 하루 한 번 정도로 호출되도록 설정한다.

entrypoint.sh 와 연관이 되므로, 파일명을 변경하지는 말 것.
"""
import time
from datetime import timedelta
import pandas as pd
import aistock.database as aistock_database
from CSV.Class_Strategies import Strategies as st
from CSV.Class_Strategies import get_stocks


def update():
    """
    데이터베이스에 저장하는 함수
    """
    # 디비 커넥션
    engine = aistock_database.connect_local()

    # ################### 모멘텀 1 mo #########################
    start = time.time()
    print("모멘텀 1 csv")
    
    # 모멘텀 1 month
    momentum_1month_rank = st.momentum_1month()
    momentum_1mo_assets = momentum_1month_rank.index[:30]
    
    # 테이블에 저장
    df = pd.DataFrame(momentum_1mo_assets, columns=['ticker'])

    print(df)

    df.to_sql('strategy_momentum_1mo', con=engine, if_exists='replace', index=False)

    # 시간 체크
    print(timedelta(seconds=(time.time() - start)))
    return

    # ################### 모멘텀 3개월 ##########################
    start = time.time()
    print("모멘텀 3 csv")

    # 모멘텀 3 month
    momentum_3months_rank = st.momentum_3months()
    momentum_3mos_assets = momentum_3months_rank.index[:30]

    # 테이블에 저장
    df = pd.DataFrame(momentum_3mos_assets, columns=['ticker'])
    df.to_sql('strategy_momentum_3mo', con=engine, if_exists='replace', index=False)
    
    # 시간 체크
    print(timedelta(seconds=(time.time() - start)))

    # ###################### 급등주 ############################
    start = time.time()
    print("급등주 csv")

    # 급등주
    speedy_rising_volume_assets = st.run()

    # 테이블에 저장
    df = pd.DataFrame(speedy_rising_volume_assets, columns=['ticker'])
    df.to_sql('strategy_soaring', con=engine, if_exists='replace', index=False)

    # 시간 체크
    print(timedelta(seconds=(time.time() - start)))

    # #################### 하루 상승빈도 ########################
    start = time.time()
    print("하루 상승빈도 csv")

    # 상승일 빈도 높은 수
    up_down_zero_df = st.get_up_down_zero_df()['종목 코드']

    # 테이블에 저장
    df = pd.DataFrame(up_down_zero_df, columns=['ticker'])
    df.to_sql('strategy_soaring_daily', con=engine, if_exists='replace', index=False)
    
    # 시간 체크
    print(timedelta(seconds=(time.time() - start)))

    # ################### Dual Momentum #######################
    start = time.time()
    print("Dual Momentum csv")
    
    # 듀얼 모멘텀
    stock_dual = get_stocks()
    prices = st.getCloseDatafromList('2021-01-01')
    dualmomentumlist = st.dual_momentum(prices, lookback_period=20, n_selection=len(stock_dual) // 2)

    # 테이블에 저장
    df = pd.DataFrame(dualmomentumlist, columns=['ticker'])
    df.to_sql('strategy_dualmomentum', con=engine, if_exists='replace', index=False)

    # 시간 체크
    print(timedelta(seconds=(time.time() - start)))


if __name__ == '__main__':
    update()
