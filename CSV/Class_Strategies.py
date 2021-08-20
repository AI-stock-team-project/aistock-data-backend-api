import pandas as pd
import FinanceDataReader as fdr
from pykrx import stock
import datetime
import warnings
warnings.filterwarnings(action='ignore')

today = datetime.datetime.today().strftime("%Y%m%d")
kospi = stock.get_market_fundamental_by_ticker(today, market='KOSPI').index
kosdaq = stock.get_market_fundamental_by_ticker(today, market='KOSDAQ').index
stocks = kospi.append(kosdaq)
#
# with open('stocks.csv', 'w') as file:
#     write = csv.writer(file)
#     write.writerow(stocks)

# stocks = pd.read_csv('stocks.csv')


class Strategies:
    def __init__(self, code_instance, stocks_1mo, stocks_3mos, code_updown, stocks_updown, index_name, start_date, bool_var,
                 prices, lookback_period, n_selection):
        self.code_instance = code_instance
        self.stocks_1mo = stocks_1mo
        self.stocks_3mos = stocks_3mos
        self.code_updown = code_updown
        self.stocks_updown = stocks_updown
        self.indexName = index_name
        self.start_date = start_date
        self.bool_var = bool_var
        self.prices = prices
        self.lookback_period = lookback_period
        self.n_selection = n_selection

# ---------------------------------------------------------------------------------------- #
    # 급등주 함수
    def check_speedy_rising_volume_yesterday(self, code_instance):  # 어제를 기준으로
        today = datetime.datetime.today().strftime("%Y%m%d")
        df = fdr.DataReader(code_instance, '2020-01-01')
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

    # 어제 거래량이 1000% 오늘 종목 찾기
    def run(self):
        speedy_rising_volume_list = []
        num = len(stocks)

        for i, code_instance in enumerate(stocks):
            if Strategies.check_speedy_rising_volume_yesterday(i, code_instance): # i 를 넣지 않으면 missing 1 requirement 계속 뜸. 급등주:  025860 7/30일
                #print("급등주: ", code_instance)
                #print(i) # 209 355 이게 뭐지??
                speedy_rising_volume_list.append(code_instance)
        return speedy_rising_volume_list
# ------------------------------------------------------------------------------- #
    # 모멘텀 1개월 함수
    def momentum_1month(self):  # 종목 list넣으면, 모멘텀 순위 있는 데이터프레임 출력
        df_momentum = pd.DataFrame()

        for s in stocks : #Strategies.today_stocks():
            df_momentum[s] = fdr.DataReader(s, '2021-01-01')['Close']

        # 20 영업일 수익률
        return_df = df_momentum.pct_change(20)
        return_df

        # 오늘 날짜
        today = datetime.datetime.today().strftime("%Y-%m-%d")

        # index는 종목 코드이고 모멘텀 데이터 있는 데이터 프레임으로 만들기
        s = return_df.loc[today]
        momentum_df = pd.DataFrame(s)
        momentum_df.columns = ["모멘텀"]

        momentum_df['순위'] = momentum_df['모멘텀'].rank(ascending=False)
        momentum_df = momentum_df.sort_values(by='순위')
        return momentum_df  # 모멘텀

    # 모멘텀 3개월 함수
    def momentum_3months(self):  # 종목 list넣으면, 모멘텀 순위 있는 데이터프레임 출력
        df = pd.DataFrame()
        for s in stocks:
            df[s] = fdr.DataReader(s, '2021-01-01')['Close']

        # 60 영업일 수익률
        return_df = df.pct_change(60)
        return_df

        # 오늘 날짜
        today = datetime.datetime.today().strftime("%Y-%m-%d")

        # index는 종목 코드이고 모멘텀 데이터 있는 데이터 프레임으로 만들기
        s = return_df.loc[today]
        momentum_df = pd.DataFrame(s)
        momentum_df.columns = ["모멘텀"]

        momentum_df['순위'] = momentum_df['모멘텀'].rank(ascending=False)
        momentum_df = momentum_df.sort_values(by='순위')
        return momentum_df  # 모멘텀
# -------------------------------------------------------------------------------- #
    # 하루 상승빈도 함수 2개
    def up_down_zero(code_updown):  # 종목과 연도에 맞는 상승/하락/변동 없는 날 수를 리스트 반환
        today = datetime.datetime.today().strftime("%Y-%m-%d")
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

    def get_up_down_zero_df(self):  # stocks 리스트를 넣으면, 상승/하락/변동없는 확률 데이터프레임 반환
        up_list = []
        down_list = []
        zero_list = []
        for i in stocks:
            temp = Strategies.up_down_zero(i)
            up_list.append(temp[0])
            down_list.append(temp[1])
            zero_list.append(temp[2])

        # 데이터 프레임 만들기
        up_down_zero_df = pd.DataFrame()
        up_down_zero_df['종목 코드'] = stocks  # 종목코드
        up_down_zero_df['상승 확률'] = up_list  # 일간 변동률이 양수인 날의 수
        up_down_zero_df['하락 확률'] = down_list  # 일간 변동률이 음수인 날의 수
        up_down_zero_df['변동 없는 확률'] = zero_list  # 일간 변동률이 0인 날의 수

        up_down_zero_df['상승 확률 높은 순위'] = up_down_zero_df['상승 확률'].rank(ascending=False)
        up_down_zero_df = up_down_zero_df.sort_values(by='상승 확률 높은 순위')
        return up_down_zero_df
# ------------------------------- 듀얼 모멘텀 함수들 -----------------------------#
    # 홀딩 리스트 가져오기
    def getHoldingsList(indexName):
        stocks = list(fdr.StockListing(indexName)['Symbol'] )# 나스닥
        return stocks[:30] # 갯수 바꿀 수 있음!!

    # stock_dual = Strategies.getHoldingsList('KOSPI')

    # 리스트를 데이터프레임으로 바꾸기
    def getCloseDatafromList(stock_dual, start_date):
        df = pd.DataFrame()
        for s in Strategies.getHoldingsList('KOSPI'):
            df[s] = fdr.DataReader(s, start_date)['Close']
        return df

    # prices = Strategies.getCloseDatafromList(stock_dual, '2021-01-01')

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
        if bool_var == True:
            result = 1
        elif bool_var == False:
            result = 0
        return result


    def DualMomentum(prices, lookback_period, n_selection):
        # lookback_period: 몇개월 모멘텀 이용할건지
        # n_selection: Top 몇개의 종목을 선택할건지(상대모멘텀)

        # absolute momentum
        returns = prices.pct_change(periods=lookback_period).fillna(0) # return 값이 true or false 로 나옴.
        long_signal = (returns > 0).applymap(Strategies.bool_converter) # applymap :dataframe.applymap(func) 괄호 없애야 함.  # 리턴값이 양수가 맞으면 1로 바꿔라
        abs_signal = long_signal[-1:]

        # relative momentum
        returns = prices.pct_change(periods=lookback_period).fillna(0)
        rank = returns.rank(axis=1, ascending=False)
        long_signal = (rank <= n_selection).applymap(Strategies.bool_converter)
        rel_signal = long_signal[-1:]

        # Dual momentum
        signal = (abs_signal == rel_signal).applymap(Strategies.bool_converter) * abs_signal
        dual_momentum_list = list(signal[signal == 1].dropna(axis=1).columns)
        return dual_momentum_list