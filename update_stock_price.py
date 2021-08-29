# noinspection PyUnresolvedReferences
from datetime import timedelta, datetime, date
from aistock.StockPrice import get_minmax_date, fetch_prices_by_dates


def update_prices(begin_date: str):
    """
    지정일 부터 현재까지(어제까지)의 주가 정보를 가져와서 테이블에 넣는 함수
    """
    print('[update stock price table] >> ', begin_date)
    (min_date_str, max_date_str) = get_minmax_date()
    if min_date_str is None:
        min_datetime = None
        max_datetime = None
    else:
        min_datetime = date.fromisoformat(min_date_str)
        max_datetime = date.fromisoformat(max_date_str)

    begin_datetime = date.fromisoformat(begin_date)
    # today = datetime.datetime.today().strftime('%Y-%m-%d')
    # today = date.today()
    yesterday = date.today() - timedelta(days=1)
    end_datetime = yesterday

    if min_datetime is None:
        start = begin_datetime
        end = end_datetime
        fetch_prices_by_dates(start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))

    else:
        if begin_datetime >= min_datetime and max_datetime == end_datetime:
            # 기준을 일단 어제로 변경... 어제까지 한정으로 데이터를 적재하도록...
            # 시작일자부터 데이터가 이미 있고, 최근 데이터도 오늘날짜와 동일한 경우. 데이터를 추가할 필요가 없음.
            print("데이터가 충분하므로 종료")
            return True

        if begin_datetime < min_datetime:
            # begin 지점이 min 보다 더 과거라면, 과거의 정보도 별도로 조회하기.
            start = begin_datetime
            end = min_datetime - timedelta(days=1)
            # print(start, end)
            fetch_prices_by_dates(start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))

        if max_datetime < end_datetime:
            # max 다음날부터 오늘까지 조회 시작
            start = max_datetime + timedelta(days=1)
            # end = today
            end = end_datetime
            # print(start, end)
            fetch_prices_by_dates(start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))

        return True


if __name__ == '__main__':
    update_prices('2021-08-24')
    print('<< [update stock price table]')
