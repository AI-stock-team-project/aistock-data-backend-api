from pathlib import Path
from datetime import timedelta, datetime, timezone
import aistock.StrategyStock as StrategyStock


def test():
    mo1 = StrategyStock.retrive_strategy_stocks_rank_with_name('mo_1')
    # mo3 = StrategyStock.retrive_strategy_stocks_rank('mo_3')
    # soaring = StrategyStock.retrive_strategy_stocks_rank('soaring')
    # up_freq = StrategyStock.retrive_strategy_stocks_rank('up_freq')
    # dual_mo = StrategyStock.retrive_strategy_stocks_rank('dual_mo')

    mo1 = mo1[['ticker', 'rank', 'name']]
    mo1 = mo1.to_dict(orient='records')
    print(mo1)


if __name__ == '__main__':
    test()
