import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import FinanceDataReader as fdr
import datetime
from dateutil.relativedelta import relativedelta # 몇달 전, 몇달 후, 몇년 전, 몇년 후 를 구하고 싶다면 relativedelta
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
import warnings
warnings.filterwarnings(action='ignore')


# 하루 상승빈도
# up_down_zero_df = st.get_up_down_zero_df()
# up_down_zero_df.to_csv("up_down_zero_df.csv")
up_down_zero_df = pd.read_csv("up_down_zero_df.csv")
up_down_zero_df.index = up_down_zero_df['Unnamed: 0']
up_down_zero_df = up_down_zero_df.drop('Unnamed: 0', axis=1)
idx_list = up_down_zero_df.index[:30]
symbol_udz = [] # 종목 코드만 가져오기
for i in idx_list:
    symbol_udz.append(up_down_zero_df.loc[i][0])

def Updown_sharpe():
    # 종목 이름 및 코드
    kospi_temp = fdr.StockListing('KOSPI')[['Symbol', 'Name']]
    kosdaq_temp = fdr.StockListing('KOSDAQ')[['Symbol', 'Name']]
    code_name_dict = pd.concat([kospi_temp, kosdaq_temp])
    code_name_dict = code_name_dict.set_index('Symbol').to_dict().get('Name')  # {'095570': 'AJ네트웍스',

    assets = np.array(symbol_udz, dtype='object')
    start_date = datetime.datetime.today() - relativedelta(years=3)
    start_date = start_date.strftime('%Y%m%d')
    # start_date = '2018-08-13'
    today = datetime.datetime.today().strftime("%Y%m%d")
    end_date = today
    df = pd.DataFrame()

    for s in assets:
        df[s] = fdr.DataReader(s, start_date, end_date)['Close']

    # drop null
    dfnull = df.dropna(axis=1)

    # 수익률의 공분산
    mu = expected_returns.mean_historical_return(dfnull)
    S = risk_models.sample_cov(dfnull)
    # print(plotting.plot_covariance(S))

    # 포폴 최적화 (Max sharp ratio) - 급등주
    ef = EfficientFrontier(mu, S, solver="SCS")
    weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    print(ef.portfolio_performance(verbose=True))

    one_million = 1000000
    portfolio_val = 15 * one_million
    latest_prices = get_latest_prices(dfnull)
    weights = cleaned_weights
    da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=portfolio_val)
    allocation, leftover = da.lp_portfolio(verbose=False)
    rmse = da._allocation_rmse_error(verbose=False)

    # 각 종목별 실제 투자 금액
    inv_total_price = {}
    for i in allocation.keys():
        inv_total_price[i] = latest_prices.loc[i] * allocation[i]
    inv_total_price

    # 총 투자금액
    investment = 0
    for i in inv_total_price.values():
        investment += i
    print(investment)

    # 각 종목별 실제 투자 비중
    inv_total_weight = {}
    for i in allocation.keys():
        inv_total_weight[i] = inv_total_price[i] / investment
    inv_total_weight

    # 투자비중의 합계
    investment_w = 0
    for i in inv_total_weight.values():
        investment_w += i
    print(investment_w)

    # 결과값으로 불러올 값을 리스트로 저장
    name_list = []  # 종목명(회사이름)
    total_price_stock = []  # 각 종목별 실제 투자 금액
    total_weight_stock = []  # 각 종목별 실제 투자 비중
    for i in allocation.keys():  # i = 포트폴리오에 할당된 종목의 종목코드
        name_list.append(code_name_dict.get(i))
        total_price_stock.append(inv_total_price.get(i))
        total_weight_stock.append(inv_total_weight.get(i))

    # Get the discrete allocation values
    discrete_allocation_list = []
    for symbol in allocation:
        discrete_allocation_list.append(allocation.get(symbol))
    print(discrete_allocation_list)

    portfolio_df = pd.DataFrame(columns=['종목명', '종목코드', '수량(주)', '투자금액(원)', '투자비중'])
    portfolio_df['종목명'] = name_list
    portfolio_df['종목코드'] = allocation
    portfolio_df['수량(주)'] = discrete_allocation_list
    portfolio_df['투자금액(원)'] = total_price_stock
    portfolio_df['투자비중'] = total_weight_stock
    portfolio_df_sorted = portfolio_df.sort_values('투자비중', ascending=False)
    portfolio_df_sorted = portfolio_df_sorted.reset_index(drop=True)
    # 투자 금액에 따라 최적화된 포트폴리오 종목별 수량
    portfolio_df_sorted.loc["합계", 2:] = portfolio_df_sorted.sum()

    ################# 코스피랑 비교 ####################
    # 각 일자별, 종목별 종가에 해당 weights를 곱해주기
    for i, weight in cleaned_weights.items():
        dfnull[i] = dfnull[i] * weight

    # 일자별 종목의 (종가*비중) 합계를 Port열에 저장
    dfnull['Port'] = dfnull.sum(axis=1)

    # 일자별 종가의 전일대비 변동률(수익률)을 portfolio라는 데이터프레임으로 저장
    portfolio = dfnull[['Port']].pct_change()

    # 코스피지수 불러오기
    kospi = fdr.DataReader('KS11', start_date, end_date)[['Close']]

    # 코스피지수의 변동률(수익률) 구하기
    # 변동률(수익률) = (당일가격-전일가격) / 전일가격
    # 7/20의 변동률(수익률) = (7/20 가격-7-19 가격) / 7/19 가격
    kospi_pct = kospi.pct_change()

    # 코스피와 포트폴리오 합치기
    result = kospi_pct.join(portfolio)

    # 1열을 0으로 (Nan 값을 0으로)
    result.iloc[0] = 0

    # 열 이름 변경
    result.columns = ['KOSPI', 'PORTFOLIO']

    # 1에서 시작해서, 전일대비 변동률(수익률)을 적용하여 수치화하기
    wealth = (1 + result).cumprod()

    # 포트폴리오와 KOSPI 지수의 '누적 수익률 추이'를 시각화하여 비교

    # matplotlib.pyplot 스타일시트 설정
    plt.style.use('fivethirtyeight')

    plt.figure(figsize=(18, 5))
    plt.plot(wealth.index, wealth.KOSPI, 'r', label='KOSPI')
    plt.plot(wealth.index, wealth.PORTFOLIO, 'b', label="PORTFOLIO(Up.Down.Zero)")
    plt.grid(True)
    plt.title('Return Trend')
    plt.xlabel('Date', fontsize=18, labelpad=7)
    plt.ylabel('Return', fontsize=18, labelpad=7)
    plt.legend(loc='best')
    plt.savefig('Updown_sharpe_return.png', dpi=100)
    plt.show()

    # 변동률 비교
    plt.figure(figsize=(18, 10))

    plt.subplot(2, 1, 1)
    plt.title('Volatility Trend')

    plt.plot(result.index, result.KOSPI, 'r', label='KOSPI')
    plt.yticks([-0.15, -0.10, -0.05, 0.00, 0.05, 0.10, 0.15])
    plt.grid(True)
    plt.ylabel('Volatility', fontsize=18, labelpad=7)
    plt.legend(loc='best')

    plt.subplot(2, 1, 2)
    plt.title('Volatility Trend')
    plt.plot(result.index, result.PORTFOLIO, 'b', label="PORTFOLIO(Up.Down.Zero)")
    plt.yticks([-0.15, -0.10, -0.05, 0.00, 0.05, 0.10, 0.15])
    plt.ylabel('Volatility', fontsize=18, labelpad=7)
    plt.legend(loc='best')

    plt.grid(True)
    plt.savefig('Updown_sharpe_votality.png', dpi=100)
    plt.show()

    # print(portfolio_df_sorted) # 데이터 프레임 출력시 시간이 걸림.

    print('----- Up.Down.Zero portfolio performance -----')
    # Show Funds Remaining
    print('Funds Remaining: ', leftover, ' KRW')

    # Show Portfolio performance
    print(ef.portfolio_performance(verbose=True))