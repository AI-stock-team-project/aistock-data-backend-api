from Class_Strategies import Strategies as st
from Class_Strategies import get_stocks
import pandas as pd
from pykrx import stock
from datetime import datetime, timedelta


def test():
    stocklist = get_stocks()
    # print(stocklist)
    df = pd.DataFrame()
    df['종목 코드'] = stocklist  # 종목코드
    print(df)
    # print(len(stocklist))
    # for i, r in stocklist.iterrows():
    #    print(type(str(r[0])))
    #    # print(type(r))
    #    # print(r)
    # stocks = load_stocks()

    # print(stocks)

    return
    # stocks = get_stocks()
    # today = '2021-08-20'
    # kospi = stock.get_market_fundamental_by_ticker(today, market='KOSPI').index
    # kosdaq = stock.get_market_fundamental_by_ticker(today, market='KOSDAQ').index
    # stocks = kospi.append(kosdaq)

    # print(type(stocks))
    # print(stocks)
    # s = stocks.reset_index(drop=True).squeeze()
    # print(type(s))
    # df = pd.DataFrame()
    # df['code'] = stocks


if __name__ == '__main__':
    test()
