import datetime


def today(f: str = "%Y-%m-%d"):
    datetime.datetime.today().strftime(f)
