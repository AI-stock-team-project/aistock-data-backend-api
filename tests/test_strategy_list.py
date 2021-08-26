# ##################### CSV 만들어서 저장하는 파일 ####################
import pandas as pd
import csv
import strategy.Strategies as st
from strategy.Strategies import get_stocks
import time
from datetime import timedelta


def test():
    mo1()


def mo1():
    """
    모멘텀 1개월
    """
    start = time.time()
    print("모멘텀 1 csv")

    momentum_1month_rank = st.momentum_1month()
    momentum_1mo_assets = momentum_1month_rank.index[:30]

    # momentum_1mo_assets.to_csv('momentum_1mo_assets.csv')
    with open('momentum_1mo_assets.csv', 'w') as file:
        write = csv.writer(file)
        write.writerow(momentum_1mo_assets)

    print(timedelta(seconds=(time.time() - start)))


def mo3():
    # ################### 모멘텀 3개월 ##########################
    start = time.time()
    print("모멘텀 3 csv")
    momentum_3months_rank = st.momentum_3months()
    momentum_3mos_assets = momentum_3months_rank.index[:30]

    with open('momentum_3mos_assets.csv', 'w') as file:
        write = csv.writer(file)
        write.writerow(momentum_3mos_assets)

    print(timedelta(seconds=(time.time() - start)))


def speedy():
    # ###################### 급등주 ############################
    start = time.time()
    print("급등주 csv")

    speedy_rising_volume_list_df = pd.DataFrame({'speedy_rising_volume_list': st.run()})
    speedy_rising_volume_list_df.to_csv("speedy_rising_volume_list_df.csv")

    print(timedelta(seconds=(time.time() - start)))


def date_count():
    # #################### 하루 상승빈도 ########################
    start = time.time()
    print("하루 상승빈도 csv")
    up_down_zero_df = st.get_up_down_zero_df()
    up_down_zero_df.to_csv("up_down_zero_df.csv")
    print(timedelta(seconds=(time.time() - start)))
    # # 대충 10분 혹은 그 이상 정도 걸림 ##


def dual_mo():
    # ################### Dual Momentum #######################
    start = time.time()
    print("Dual Momentum csv")
    # stock_dual = st.get_holding_list('KOSPI')
    stock_dual = get_stocks()
    prices = st.get_close_prices_all('2021-01-01')
    dualmomentumlist = st.dual_momentum(prices, lookback_period=20, n_selection=len(stock_dual) // 2)

    with open('dualmomentumlist.csv', 'w') as file:
        write = csv.writer(file)
        write.writerow(dualmomentumlist)
    print(timedelta(seconds=(time.time() - start)))


if __name__ == '__main__':
    test()
