###################### CSV 만들어서 저장하는 파일 ####################
import pandas as pd
import warnings
warnings.filterwarnings(action='ignore')
from Class_Strategies import Strategies as st
import csv

####################### 급등주 ############################
speedy_rising_volume_list_df = pd.DataFrame({'speedy_rising_volume_list':st.run()})
speedy_rising_volume_list_df.to_csv("speedy_rising_volume_list_df.csv")

#################### 모멘텀 1 mo #########################
momentum_1month_rank  = st.momentum_1month()
momentum_1mo_assets = momentum_1month_rank.index[:30]

with open('momentum_1mo_assets.csv','w') as file:
    write = csv.writer(file)
    write.writerow(momentum_1mo_assets)

#################### 모멘텀 3개월 ##########################
momentum_3months_rank  = st.momentum_3months()
momentum_3mos_assets = momentum_3months_rank.index[:30]

with open('momentum_3mos_assets.csv','w') as file:
    write = csv.writer(file)
    write.writerow(momentum_3mos_assets)

#################### Dual Momentum #######################
stock_dual = st.getHoldingsList('KOSPI')
prices = st.getCloseDatafromList(stock_dual, '2021-01-01')
dualmomentumlist = st.DualMomentum(prices, lookback_period = 20, n_selection = len(stock_dual)//2)

with open('dualmomentumlist.csv','w') as file:
    write = csv.writer(file)
    write.writerow(dualmomentumlist)

##################### 하루 상승빈도 ########################
up_down_zero_df = st.get_up_down_zero_df()
up_down_zero_df.to_csv("up_down_zero_df.csv")

## 대충 10분 혹은 그 이상 정도 걸림 ##
