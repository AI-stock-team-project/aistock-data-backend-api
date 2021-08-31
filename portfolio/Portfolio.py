from datetime import datetime
from enum import Enum
from pathlib import Path

import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import pandas as pd
from dateutil.relativedelta import relativedelta
from pypfopt import expected_returns
from pypfopt import risk_models
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
from pypfopt.efficient_frontier import EfficientFrontier

import aistock.StockReader as StockReader
import aistock.StrategyStock as StrategyStock
from aistock.StockPrice import get_close_prices_by, StockPriceTable
from aistock.StrategyStock import StrategyCode


class OptimizeMethod(Enum):
    """
    최적화 방법 종류
    """
    Efficient = 1
    MaxSharpe = 2

    def __str__(self):
        return self.name


class AssetMethod(Enum):
    """
    종목 선택 방법 종류
    """
    # 종목 선택
    CUSTOM = 1
    # 듀얼모멘텀
    DUAL_MOMENTUM = 2
    # 급등주
    SOARING = 3
    # 모멘텀 1개월
    MOMENTUM_1MONTH = 4
    # 모멘텀 3개월
    MOMENTUM_3MONTH = 5
    # 상승하는 날의 빈도가 높음
    UP_FREQ = 6

    def __str__(self):
        if self.value == self.CUSTOM.value:
            return 'Custom'
        elif self.value == self.DUAL_MOMENTUM.value:
            return 'Dual Momentum'
        elif self.value == self.SOARING.value:
            return 'Speedy Rising'
        elif self.value == self.MOMENTUM_1MONTH.value:
            return 'Momentum 1month'
        elif self.value == self.MOMENTUM_3MONTH.value:
            return 'Momentum 3month'
        elif self.value == self.UP_FREQ.value:
            return 'Up.Down.Zero'
        else:
            return ''


def get_assets(method, custom_assets=None) -> list:
    """
    종목을 가져옴.
    """
    if method == AssetMethod.CUSTOM:
        # 국내 종목(삼성전자, SK하이닉스, 카카오, NAVER, LG화학 ) - 웹에 연결시 선택한 종목이 assets 에 들어가면 됨.
        # assets = ['005930', '000660', '035720', '035420', '051910']
        return custom_assets

    if method == AssetMethod.DUAL_MOMENTUM:
        strategy_code = StrategyCode.dual_momentum
    elif method == AssetMethod.SOARING:
        strategy_code = StrategyCode.soaring
    elif method == AssetMethod.MOMENTUM_1MONTH:
        strategy_code = StrategyCode.mementum_1month
    elif method == AssetMethod.MOMENTUM_3MONTH:
        strategy_code = StrategyCode.mementum_3month
    elif method == AssetMethod.UP_FREQ:
        strategy_code = StrategyCode.up_freq
    else:
        raise

    assets = StrategyStock.get_strategy_stocks_to_list(strategy_code)
    return assets


def make_portfolio(optimize_method=OptimizeMethod.Efficient, asset_method=AssetMethod.DUAL_MOMENTUM,
                   years=3, money=15000000, risk_limit=0.3, assets: list = None):
    """

    :param optimize_method: 포트폴리오 최적화 방법 선택
    :param asset_method: 종목 가져오는 방법 선택
    :param years: 투자 기간
    :param money: 투자 금액
    :param risk_limit: 감당 리스크
    :param assets: 종목 선택
    :return:
    """
    # ============= 파라미터 조정 및 체크 ===========
    if assets is None:
        raise

    # 투자 금액
    param_money = money
    # 감당 리스크
    param_risk_limit = risk_limit
    # 종목 (list 형)
    param_assets = assets

    # ============== 구문 시작 ==============
    kospi_temp = fdr.StockListing('KOSPI')[['Symbol', 'Name']]
    kosdaq_temp = fdr.StockListing('KOSDAQ')[['Symbol', 'Name']]
    code_name_dict = pd.concat([kospi_temp, kosdaq_temp])
    code_name_dict = code_name_dict.set_index('Symbol').to_dict().get('Name')

    # 기간 설정
    start_date = datetime.today() - relativedelta(years=years)
    start_date = start_date.strftime('%Y-%m-%d')
    today = datetime.today().strftime("%Y-%m-%d")
    end_date = today
    df = pd.DataFrame()

    for ticker in param_assets:
        # df[ticker] = fdr.DataReader(ticker, start_date, end_date)['Close']
        df[ticker] = get_close_prices_by(ticker, begin_date=start_date)[StockPriceTable.close.name]

    # drop null
    dfnull = df.dropna(axis=1)

    # 수익률의 공분산
    mu = expected_returns.mean_historical_return(dfnull)
    # noinspection PyPep8Naming
    S = risk_models.sample_cov(dfnull)
    # print(plotting.plot_covariance(S))

    # 포폴 최적화
    if optimize_method == OptimizeMethod.MaxSharpe:
        # 포폴 최적화 (Max sharpe ratio)
        ef = EfficientFrontier(mu, S, solver="SCS")

        df_t = fdr.DataReader(f'KR{years}YT=RR')
        rf_t = df_t.Close[-1]/100
        # noinspection PyUnusedLocal
        # weights = ef.max_sharpe()
        weights = ef.max_sharpe(risk_free_rate=rf_t)
    elif optimize_method == OptimizeMethod.Efficient:
        # 포폴 최적화 (Efficient Risk)
        vol_limit = param_risk_limit
        ef = EfficientFrontier(mu, S, solver="SCS")
        # noinspection PyUnusedLocal
        weights = ef.efficient_risk(vol_limit)
    else:
        print('empty portfolio optimize method!')
        raise

    # 뭔가 계산하는 듯? 뭐지?
    cleaned_weights = ef.clean_weights()
    # print(ef.portfolio_performance(verbose=True))
    expected_annual_return, annual_volatility, sharpe_ratio = ef.portfolio_performance(verbose=False)
    print("Expected annual return: {:.1f}%".format(100 * expected_annual_return))
    print("Annual volatility: {:.1f}%".format(100 * annual_volatility))
    print("Sharpe Ratio: {:.2f}".format(sharpe_ratio))

    # 투자 비중, 투자 수량 등을 계산
    portfolio_val = param_money
    latest_prices = get_latest_prices(dfnull)
    weights = cleaned_weights
    da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=portfolio_val)
    allocation, leftover = da.lp_portfolio(verbose=False)
    # noinspection PyProtectedMember,PyUnusedLocal
    rmse = da._allocation_rmse_error(verbose=False)

    # 각 종목별 실제 투자 금액
    inv_total_price = {}
    for i in allocation.keys():
        inv_total_price[i] = latest_prices.loc[i] * allocation[i]
    print(inv_total_price)

    # 총 투자금액
    investment = 0
    for i in inv_total_price.values():
        investment += i
    print(investment)

    # 각 종목별 실제 투자 비중
    inv_total_weight = {}
    for i in allocation.keys():
        inv_total_weight[i] = inv_total_price[i] / investment
    print(inv_total_weight)

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

    portfolio_df = pd.DataFrame(columns=['name', 'symbol', 'number', 'money', 'weight'])
    portfolio_df['name'] = name_list  # 종목명
    portfolio_df['symbol'] = allocation  # 종목코드
    portfolio_df['number'] = discrete_allocation_list  # 수량 (주)
    portfolio_df['money'] = total_price_stock  # 투자금액 (원)
    portfolio_df['weight'] = total_weight_stock  # 투자 비중
    portfolio_df_sorted = portfolio_df.sort_values('weight', ascending=False)
    portfolio_df_sorted = portfolio_df_sorted.reset_index(drop=True)
    # 투자 금액에 따라 최적화된 포트폴리오 종목별 수량
    portfolio_df_sorted.loc["sum", 2:] = portfolio_df_sorted.sum()
    # portfolio_df_sorted.loc["sum", 'name'] = 'sum'

    # ################ 코스피랑 비교 ####################
    # 각 일자별, 종목별 종가에 해당 weights를 곱해주기
    for i, weight in cleaned_weights.items():
        dfnull[i] = dfnull[i] * weight

    # 일자별 종목의 (종가*비중) 합계를 Port열에 저장
    dfnull['Port'] = dfnull.sum(axis=1)

    # 일자별 종가의 전일대비 변동률(수익률)을 portfolio라는 데이터프레임으로 저장
    portfolio = dfnull[['Port']].pct_change()

    # 코스피지수 불러오기
    # kospi = fdr.DataReader('KS11', start_date, end_date)[['Close']]
    kospi = StockReader.read_index_by('kospi', start_date, end_date)[['Close']]

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

    # ############ --------- 시각화 -------- ############
    static_path = Path(__file__).resolve().parent.parent / 'static'
    static_url = '/static/'
    dt_now = datetime.now().strftime('%Y%m%d_%H%M%S')
    trends_file_path = static_path / f'return_trends_{dt_now}.png'
    votality_file_path = static_path / f'votality_trends_{dt_now}.png'
    trends_file_url = static_url + f'return_trends_{dt_now}.png'
    votality_file_url = static_url + f'votality_trends_{dt_now}.png'
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
    plt.savefig(trends_file_path, dpi=100)
    # plt.show()

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
    plt.savefig(votality_file_path, dpi=100)
    # plt.show()
    # ############# ------------print------------- #####################
    print(f'----- {str(asset_method)} portfolio performance -----')
    # Show Funds
    print('Funds:', portfolio_val, 'KRW')

    # Show Funds Remaining
    print('Funds Remaining: ', leftover, ' KRW')

    # Show Portfolio performance
    print(ef.portfolio_performance(verbose=True))
    # noinspection PyProtectedMember
    rmse = da._allocation_rmse_error(verbose=False)
    print(rmse)

    return {
        'expected_annual_return': expected_annual_return,
        'annual_volatility': annual_volatility,
        'sharpe_ratio': sharpe_ratio,
        'balance': leftover,
        'trends_file_url': trends_file_url,
        'votality_file_url': votality_file_url
    }, portfolio_df_sorted
