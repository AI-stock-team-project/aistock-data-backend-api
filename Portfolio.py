from enum import Enum

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
import numpy as np
warnings.filterwarnings(action='ignore')


class OptimizeMethod(Enum):
    """
    최적화 방법 종류
    """
    Efficient = 1
    MaxSharp = 2

    def __str__(self):
        return self.name


class AssetMethod(Enum):
    """
    종목 선택 방법 종류
    """
    # 종목 선택
    CUSTOM = 1
    # 듀얼모멘텀
    DUAL = 2
    # 급등주
    SOARING = 3
    # 모멘텀 1개월
    MOMENTUM_1MONTH = 4
    # 모멘텀 3개월
    MOMENTUM_3MONTH = 5
    # 상승하는 날의 빈도가 높음
    DATE_COUNT = 6

    def __str__(self):
        if self.value == self.CUSTOM.value:
            return ''
        elif self.value == self.DUAL.value:
            return 'Dual Momentum'
        elif self.value == self.SOARING.value:
            return 'Speedy Rising'
        elif self.value == self.MOMENTUM_1MONTH.value:
            return 'Momentum 1month'
        elif self.value == self.MOMENTUM_3MONTH.value:
            return 'Momentum 3month'
        elif self.value == self.DATE_COUNT.value:
            return 'Up.Down.Zero'
        else:
            return ''


def get_assets(method, custom_assets=None):
    """
    종목을 가져옴.
    """
    if method == AssetMethod.CUSTOM:
        # 국내 종목(삼성전자, SK하이닉스, 카카오, NAVER, LG화학 ) - 웹에 연결시 선택한 종목이 assets 에 들어가면 됨.
        # assets = ['005930', '000660', '035720', '035420', '051910']
        return custom_assets
    elif method == AssetMethod.DUAL:
        assets = pd.read_csv('CSV/dualmomentumlist.csv')  # np.array(dualmomentumlist)
    elif method == AssetMethod.SOARING:
        df = pd.read_csv('CSV/speedy_rising_volume_list_df.csv')
        df['speedy_rising_volume_list'] = df[
            'speedy_rising_volume_list'].apply(lambda x: '{0:0>6}'.format(x))
        asset = df['speedy_rising_volume_list']
        assets = np.array(asset.values)
    elif method == AssetMethod.MOMENTUM_1MONTH:
        assets = pd.read_csv('CSV/momentum_1mo_assets.csv')
    elif method == AssetMethod.MOMENTUM_3MONTH:
        assets = pd.read_csv('CSV/momentum_3mos_assets.csv')
    elif method == AssetMethod.DATE_COUNT:
        up_down_zero_df = pd.read_csv("CSV/up_down_zero_df.csv")
        up_down_zero_df.index = up_down_zero_df['Unnamed: 0']
        up_down_zero_df = up_down_zero_df.drop('Unnamed: 0', axis=1)
        idx_list = up_down_zero_df.index[:30]
        symbol_udz = []  # 종목 코드만 가져오기
        for i in idx_list:
            symbol_udz.append(up_down_zero_df.loc[i][0])
        assets = np.array(symbol_udz, dtype='object')
    else:
        raise
    return assets


def make_portfolio(optimize=OptimizeMethod.Efficient, asset_method=AssetMethod.DUAL,
                   year=3, money=15000000, risk_limit=0.3, custom_assets=None):
    # ============== 파라미터 부분 ==============
    # 포트폴리오 최적화 방법 선택
    opt_method = OptimizeMethod.Efficient
    # 종목 가져오는 방법 선택
    asset_method = AssetMethod.DUAL
    # 투자 기간
    param_year = 3
    # 투자 금액 (샘플로 1.5천만)
    param_money = 15 * 1000000
    # 감당 리스크
    param_risk_limit = 0.3

    # ============== 구문 시작 ==============
    kospi_temp = fdr.StockListing('KOSPI')[['Symbol', 'Name']]
    kosdaq_temp = fdr.StockListing('KOSDAQ')[['Symbol', 'Name']]
    code_name_dict = pd.concat([kospi_temp, kosdaq_temp])
    code_name_dict = code_name_dict.set_index('Symbol').to_dict().get('Name')

    # 종목 조회
    assets = get_assets(asset_method, custom_assets)

    # 기간 설정
    start_date = datetime.datetime.today() - relativedelta(years=param_year)
    start_date = start_date.strftime('%Y%m%d')
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

    # 포폴 최적화
    if opt_method == OptimizeMethod.MaxSharp:
        # 포폴 최적화 (Max sharp ratio)
        ef = EfficientFrontier(mu, S, solver="SCS")
        weights = ef.max_sharpe()
    elif opt_method == OptimizeMethod.Efficient:
        # 포폴 최적화 (Efficient Risk)
        vol_limit = param_risk_limit
        ef = EfficientFrontier(mu, S, solver="SCS")
        weights = ef.efficient_risk(vol_limit)
    else:
        print('empty portfolio optimize method!')
        raise

    cleaned_weights = ef.clean_weights()
    print(ef.portfolio_performance(verbose=True))

    portfolio_val = param_money
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
    plt.plot(wealth.index, wealth.PORTFOLIO, 'b', label=f"PORTFOLIO({str(asset_method)})")
    plt.grid(True)
    plt.title('Return Trend')
    plt.xlabel('Date', fontsize=18, labelpad=7)
    plt.ylabel('Return', fontsize=18, labelpad=7)
    plt.legend(loc='best')
    plt.savefig('return_trends.png', dpi=100)
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
    plt.plot(result.index, result.PORTFOLIO, 'b', label=f"PORTFOLIO({str(asset_method)})")
    plt.yticks([-0.15, -0.10, -0.05, 0.00, 0.05, 0.10, 0.15])
    plt.ylabel('Volatility', fontsize=18, labelpad=7)
    plt.legend(loc='best')

    plt.grid(True)
    plt.savefig('votality_trends.png', dpi=100)
    plt.show()

    print('----- Momentum 1month sharpe portfolio performance -----')
    # Show Funds
    print('Funds:', portfolio_val, 'KRW')

    # Show Funds Remaining
    print('Funds Remaining: ', leftover, ' KRW')

    # Show Portfolio performance
    ef.portfolio_performance(verbose=True)
    rmse = da._allocation_rmse_error(verbose=False)
    print(rmse)
