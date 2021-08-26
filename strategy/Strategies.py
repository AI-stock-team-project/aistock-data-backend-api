import pandas as pd
import FinanceDataReader as fdr
from datetime import timedelta, datetime, date
from dateutil.relativedelta import relativedelta
import aistock.StockReader as StockReader
from pandas import Series, DataFrame
from aistock.StockPrice import get_close_prices_by, StockPriceTable, get_volumes_by
# noinspection PyUnresolvedReferences
from deprecated import deprecated
import os
import warnings
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

# 글로벌 변수로 전환. 자꾸 로드하는 것을 줄일 수 있음. (큰 차이는 안 나는 듯..)
g_stocks = None


def get_stocks():
    """
    종목을 가져오기
    :return: 종목 목록 (DataFrame)
    """
    is_global_enabled = True
    is_csv_enabled = True

    if not is_global_enabled:
        # 글로벌 변수를 이용하지 않고 바로바로 로드할 경우
        return StockReader.read_tickerlist_to_list()

    else:
        global g_stocks

        if g_stocks is not None:
            return g_stocks
        else:
            if is_csv_enabled:
                csv_file: str = 'g_stock.csv'
                if os.path.exists(csv_file):
                    df = pd.read_csv(csv_file)["ticker"]
                    # print(df)
                    g_stocks = df.to_list()
                else:
                    # csv 파일 생성
                    g_stocks = StockReader.read_tickerlist_to_list()

                    df = pd.DataFrame(g_stocks, columns=["ticker"])
                    # noinspection PyTypeChecker
                    df.to_csv(csv_file, index=False)
            else:
                g_stocks = StockReader.read_tickerlist_to_list()
            return g_stocks


def get_close_prices_all(start_date):
    """
    시작일로부터 현재까지의 종가 정보 조회
    :param start_date:
    :return: DataFrame=index(날짜:y-m-d), columns(tickers)
    """
    df = pd.DataFrame()
    stocklist = get_stocks()
    for ticker in stocklist:
        # print(ticker, type(ticker))

        # 0:00:32.918956
        df[ticker] = get_close_prices_by(ticker, begin_date=start_date)[StockPriceTable.close.name]

        # 0: 01:07.990137
        # s = get_close_prices_by(ticker, begin_date=start_date)[StockPriceColumns.close]
        # df = pd.concat([df, s], axis=1)
    return df


def memontum_month(_momentum_type: str) -> DataFrame:
    """
    모멘텀 1개월/3개월 종목을 가져오는 함수
    모멘텀 순위 있는 데이터프레임 출력
    :return: DataFrame

    """
    if _momentum_type == '3month':
        start_date_before = -90
        pct_change_base = 60
    else:
        start_date_before = -40
        pct_change_base = 20

    # 여유 있게 20일 + 10일 전까지의 데이터를 조회한다.
    start_date = (datetime.now() + timedelta(days=start_date_before)).strftime('%Y-%m-%d')
    df = get_close_prices_all(start_date)
    # df = pd.DataFrame()
    # df['060310'] = get_close_prices_by('060310', begin_date='2021-07-01')['close']
    # df['265520'] = get_close_prices_by('265520', begin_date='2021-07-01')['close']

    # 20 영업일 수익률
    return_df = df.pct_change(pct_change_base)
    # print(return_df)

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
    return momentum_df.iloc[:30, :]


def momentum_1month() -> DataFrame:
    """
    모멘텀 1개월 종목을 가져오는 함수
    모멘텀 순위 있는 데이터프레임 출력
    :return: DataFrame
    """
    return memontum_month('1month')


def momentum_3months() -> DataFrame:
    """
    모멘텀 3개월 종목을 가져오는 함수
    모멘텀 순위 있는 데이터프레임 출력
    :return: DataFrame
    """
    return memontum_month('3month')


def check_speedy_rising_volume_yesterday(ticker: str) -> bool:
    """
    급등주 여부를 검사하는 함수
    어제를 기준으로 그보다 더 전의 20일간의 거래량의 평균을 구해서 비교
    :param ticker: ticker 코드
    :return: bool
    """
    start_date = (datetime.now() + timedelta(days=-45)).strftime('%Y-%m-%d')
    # df = fdr.DataReader(ticker, start_date)
    # volumes = df['Volume'].iloc[::-1]
    df = get_volumes_by(ticker, begin_date=start_date)['volume']
    volumes = df.iloc[::-1]  # iloc[::-1]은 역순정렬

    if len(volumes) < 22:  # 총 22일 치의 데이터가 없을 경우 제외(최근 상장 종목)
        return False

    sum_vol20 = 0
    # today_vol = 0
    today = datetime.today().strftime("%Y-%m-%d")
    latest_volume = None
    sum_count = 0
    for index, vol in volumes.items():
        if index.strftime('%Y-%m-%d') == today:
            continue
        elif latest_volume is None:
            latest_volume = vol
        elif sum_count < 20:
            sum_vol20 += vol
            sum_count += 1
        else:
            break

    avg_vol20 = sum_vol20 / 20  # 최근 20일간 평균 거래량 구하기
    if latest_volume > avg_vol20 * 10:  # 조회 시작일의 거래량이 평균 거래량을 1000% 초과한다면 True
        return True
    return False


def speedy_rising_volume() -> list:
    """
    어제 거래량이 1000% 오늘 종목 목록
    :return: list
    """
    speedy_rising_volume_list = []
    for ticker in get_stocks():
        if check_speedy_rising_volume_yesterday(ticker):
            speedy_rising_volume_list.append(ticker)
    return speedy_rising_volume_list


def up_down_zero(code_updown):
    """
    종목과 연도에 맞는 상승/하락/변동 없는 날 수를 리스트 반환
    :param code_updown:
    :return:
    """
    one_year_ago = (datetime.now() - relativedelta(years=1)).strftime('%Y-%m-%d')

    # data = fdr.DataReader(code_updown, one_year_ago)[['Close']]
    data = get_close_prices_by(code_updown, begin_date=one_year_ago)['close']

    data_rtn = data.pct_change()

    up = 0
    nothing = 0
    down = 0

    for index, pct in data_rtn.items():
        if pct > 0:
            up += 1
        elif pct == 0:
            nothing += 1
        else:
            down += 1

    """
    for i, date in enumerate(data.index):
        if data_rtn.Close.iloc[i] > 0:
            up = up + 1
        elif data_rtn.Close.iloc[i] == 0:
            nothing = nothing + 1
        else:
            down = down + 1
    """

    total_days = len(data_rtn.index)
    return up / total_days, down / total_days, nothing / total_days


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
        temp = up_down_zero(ticker)
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


@deprecated
def get_holding_list(index_name):
    """
    홀딩 리스트 가져오기
    :param index_name:
    :return:
    """
    _stocks = list(fdr.StockListing(index_name)['Symbol'])  # 나스닥
    return _stocks[:30]  # 갯수 바꿀 수 있음!!


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
