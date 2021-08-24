import datetime


def today(f: str = "%Y-%m-%d") -> str:
    datetime.datetime.today().strftime(f)
