import csv

import pandas as pd
import FinanceDataReader as fdr
from pykrx import stock
from datetime import datetime, timedelta
import aistock.StockReader as StockReader
from pandas import Series, DataFrame
import os
# today = datetime.datetime.today().strftime("%Y%m%d")
# kospi = stock.get_market_fundamental_by_ticker(today, market='KOSPI').index
# kosdaq = stock.get_market_fundamental_by_ticker(today, market='KOSDAQ').index
# stocks = kospi.append(kosdaq)
#
# with open('stocks.csv', 'w') as file:
#     write = csv.writer(file)
#     write.writerow(stocks)

# stocks = pd.read_csv('stocks.csv')
# 글로벌 변수로 전환. 자꾸 로드하는 것을 줄일 수 있음. (큰 차이는 안 나는 듯..)
g_stocks = None


def get_stocks():
    """
    종목을 가져오기
    :return: 종목 목록 (DataFrame)
    """
    is_global_enabled = True

    if not is_global_enabled:
        # 글로벌 변수를 이용하지 않고 바로바로 로드할 경우
        return StockReader.read_tickers_to_list()

    global g_stocks

    if g_stocks is not None:
        return g_stocks
    else:
        g_stocks = StockReader.read_tickers_to_list()
        return g_stocks


# 현재 듀얼 모멘텀으로 어떤 주식을 사야 하는지 리스트화
def bool_converter(bool_var):
    """Returns Integer Value from Boolean Value
    Parameters
    ----------
    bool_var : boolean
        Boolean variables representing trade signals
    Returns
    -------
    result : int
        Integer variables representing trade signals
    """
    if bool_var:
        return 1
    else:
        return 0


class Strategies:

    @staticmethod
    def check_speedy_rising_volume_yesterday(code_instance):
        """
        급등주 여부를 검사하는 함수
        어제를 기준으로 그보다 더전의 20일간의 평균을 구해서 비교
        :param code_instance: ticker 코드
        :type code_instance: str
        :return: bool
        """
        # today = datetime.today().strftime("%Y%m%d")
        start_date = (datetime.now() + timedelta(days=-30)).strftime('%Y-%m-%d')
        df = fdr.DataReader(code_instance, start_date)
        volumes = df['Volume'].iloc[::-1]

        if len(volumes) < 22:  # 총 22일 치의 데이터가 없을 경우 제외(최근 상장 종목)
            return False

        sum_vol20 = 0
        today_vol = 0

        for i, vol in enumerate(volumes):
            if i == 0:  # 오늘 날짜
                continue
            elif i == 1:  # 어제 날짜
                today_vol = vol
            elif 2 <= i <= 21:
                sum_vol20 += vol
            else:
                break

        avg_vol20 = sum_vol20 / 20  # 최근 20일간 평균 거래량 구하기
        if today_vol > avg_vol20 * 10:  # 조회 시작일의 거래량이 평균 거래량을 1000% 초과한다면 True
            return True

    @staticmethod
    def run() -> list:
        """
        어제 거래량이 1000% 오늘 종목 목록
        :return: list
        """
        speedy_rising_volume_list = []
        for ticker in get_stocks():
            if Strategies.check_speedy_rising_volume_yesterday(ticker):
                speedy_rising_volume_list.append(ticker)
        return speedy_rising_volume_list

    @staticmethod
    def momentum_1month() -> DataFrame:
        """
        모멘텀 1개월 종목을 가져오는 함수
        모멘텀 순위 있는 데이터프레임 출력
        :return: DataFrame
        """
        start_date = (datetime.now() + timedelta(days=-30)).strftime('%Y-%m-%d')
        df = Strategies.getCloseDatafromList(start_date)

        # 20 영업일 수익률
        return_df = df.pct_change(20)

        # 오늘 날짜
        # today = datetime.today().strftime("%Y-%m-%d")
        # 아 이거... 주말에는 오류가 날 수 있어서.. 마지막 값으로 보정.
        today = df.index[-1]

        # index는 종목 코드이고 모멘텀 데이터 있는 데이터 프레임으로 만들기
        s = return_df.loc[today]
        momentum_df = pd.DataFrame(s)
        momentum_df.columns = ["모멘텀"]

        momentum_df['순위'] = momentum_df['모멘텀'].rank(ascending=False)
        momentum_df = momentum_df.sort_values(by='순위')
        return momentum_df

    @staticmethod
    def momentum_3months():
        """
        모멘텀 3개월 종목을 가져오는 함수
        모멘텀 순위 있는 데이터프레임 출력
        :return: DataFrame
        """
        # df = pd.DataFrame()
        # stocks = get_stocks()
        start_date = (datetime.now() + timedelta(days=-70)).strftime('%Y-%m-%d')
        # for _code in stocks:
        #    df[_code] = fdr.DataReader(_code, start_date)['Close']
        #    # s = fdr.DataReader(_code, start_date)['Close'].rename(_code)
        #    # df = pd.concat([df, s], axis=1)
        df = Strategies.getCloseDatafromList(start_date)

        # 60 영업일 수익률
        return_df = df.pct_change(60)
        # return_df

        # 오늘 날짜
        today = datetime.today().strftime("%Y-%m-%d")

        # index는 종목 코드이고 모멘텀 데이터 있는 데이터 프레임으로 만들기
        s = return_df.loc[today]
        momentum_df = pd.DataFrame(s)
        momentum_df.columns = ["모멘텀"]

        momentum_df['순위'] = momentum_df['모멘텀'].rank(ascending=False)
        momentum_df = momentum_df.sort_values(by='순위')
        return momentum_df

    @staticmethod
    def up_down_zero(code_updown):
        """
        종목과 연도에 맞는 상승/하락/변동 없는 날 수를 리스트 반환
        :param code_updown:
        :return:
        """
        today = datetime.today().strftime("%Y-%m-%d")
        year = today[0:4]
        month_day = today[4:]
        one_year_ago = str(int(year) - 1) + month_day

        data = fdr.DataReader(code_updown, one_year_ago)[['Close']]
        data_rtn = data.pct_change()

        up = 0
        nothing = 0
        down = 0
        for i, date in enumerate(data.index):
            if data_rtn.Close.iloc[i] > 0:
                up = up + 1
            elif data_rtn.Close.iloc[i] == 0:
                nothing = nothing + 1
            else:
                down = down + 1

        total_days = len(data_rtn.index)
        return up / total_days, down / total_days, nothing / total_days

    @staticmethod
    def get_up_down_zero_df() -> DataFrame:
        """
        상승/하락/변동없는 확률 데이터프레임 반환
        :return:
        """
        up_list = []
        down_list = []
        zero_list = []
        # stocks = get_stocks()
        # for i in stocks:
        stocklist = get_stocks()
        for ticker in stocklist:
            temp = Strategies.up_down_zero(ticker)
            up_list.append(temp[0])
            down_list.append(temp[1])
            zero_list.append(temp[2])

        # 데이터 프레임 만들기
        up_down_zero_df = pd.DataFrame()
        up_down_zero_df['종목 코드'] = stocklist  # 종목코드
        up_down_zero_df['상승 확률'] = up_list  # 일간 변동률이 양수인 날의 수
        up_down_zero_df['하락 확률'] = down_list  # 일간 변동률이 음수인 날의 수
        up_down_zero_df['변동 없는 확률'] = zero_list  # 일간 변동률이 0인 날의 수

        up_down_zero_df['상승 확률 높은 순위'] = up_down_zero_df['상승 확률'].rank(ascending=False)
        up_down_zero_df = up_down_zero_df.sort_values(by='상승 확률 높은 순위')
        up_down_zero_df = up_down_zero_df.reset_index(drop=True)
        return up_down_zero_df
# ------------------------------- 듀얼 모멘텀 함수들 -----------------------------#

    @staticmethod
    def get_holding_list(index_name):
        """
        홀딩 리스트 가져오기
        :param index_name: 
        :return: 
        """
        _stocks = list(fdr.StockListing(index_name)['Symbol'])  # 나스닥
        return _stocks[:30]  # 갯수 바꿀 수 있음!!

    # stock_dual = Strategies.get_holding_list('KOSPI')

    # noinspection PyPep8Naming
    @staticmethod
    def getCloseDatafromList(start_date):
        """
        시작일로부터 현재까지의 종가 정보 조회
        :param start_date: 
        :return: DataFrame=index(날짜:y-m-d), columns(tickers)
        """
        df = pd.DataFrame()
        # for s in Strategies.get_holding_list('KOSPI'):
        stocklist = get_stocks()
        for ticker in stocklist:
            df[ticker] = fdr.DataReader(ticker, start_date)['Close']
            # s = fdr.DataReader(_code, start_date)['Close'].rename(_code)
            # df = pd.concat([df, s], axis=1)
        return df

    # prices = Strategies.getCloseDatafromList(stock_dual, '2021-01-01')

    @staticmethod
    def dual_momentum(prices, lookback_period, n_selection) -> list:
        """
        Dual Momentum
        :param prices: 가격을 갖고 있는 데이터프레임 (index:날짜, columns:티커)
        :param lookback_period: 몇개월 모멘텀 이용할건지
        :type lookback_period: int
        :param n_selection: Top 몇개의 종목을 선택할건지(상대모멘텀)
        :type n_selection: int
        :return: list
        """

        # absolute momentum
        returns = prices.pct_change(periods=lookback_period).fillna(0)  # return 값이 true or false 로 나옴.
        long_signal = (returns > 0).applymap(bool_converter)  # applymap :dataframe.applymap(func) 괄호 없애야 함.  # 리턴값이 양수가 맞으면 1로 바꿔라
        abs_signal = long_signal[-1:]

        # relative momentum
        returns = prices.pct_change(periods=lookback_period).fillna(0)
        rank = returns.rank(axis=1, ascending=False)
        long_signal = (rank <= n_selection).applymap(bool_converter)
        rel_signal = long_signal[-1:]

        # Dual momentum
        # noinspection PyUnresolvedReferences
        signal = (abs_signal == rel_signal).applymap(bool_converter) * abs_signal
        dual_momentum_list = list(signal[signal == 1].dropna(axis=1).columns)
        return dual_momentum_list
