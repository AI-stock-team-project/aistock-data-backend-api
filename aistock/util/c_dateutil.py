# noinspection PyUnresolvedReferences
from datetime import datetime, timedelta, timezone
from dateutil import tz


def today_str(f: str = "%Y-%m-%d") -> str:
    return datetime.today().strftime(f)


def utc_to_local(dt: datetime):
    """
    python-dateutil 사용
    """
    # UTC 타임이라고 지정
    dt = dt.replace(tzinfo=timezone.utc)
    # print(dt.strftime('%Y-%m-%d %H:%M:%S %Z%z'))

    # dateutil 을 사용한 방법
    rv = dt.astimezone(tz.tzlocal())
    # print(rv.strftime('%Y-%m-%d %H:%M:%S %Z%z'))
    return rv


def utc_to_kst_pytz(dt: datetime):
    """
    pytz가 있을 때, 이를 이용
    """

    try:
        import pytz
        kst = pytz.timezone('Asia/Seoul')
        utc = pytz.timezone('UTC')

        # UTC 타임이라고 지정
        d = utc.localize(dt)

        # kst로 시간 변경
        rv = d.astimezone(kst)
        # print(rv.strftime('%Y-%m-%d %H:%M:%S %Z%z'))
        return rv

    except ModuleNotFoundError:
        return ''
