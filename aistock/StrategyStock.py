import pandas as pd
# noinspection PyUnresolvedReferences
from pandas import Series, DataFrame
# noinspection PyUnresolvedReferences
from deprecated import deprecated
# noinspection PyUnresolvedReferences
from datetime import timedelta, datetime

from sqlalchemy import Column, Integer, String, select, DateTime
import aistock.database as aistock_database
from aistock.database import Base, db_session


class StrategyCode:
    dual_momentum = 'dual_mo'
    soaring = 'soaring'
    mementum_1month = 'mo_1'
    mementum_3month = 'mo_3'
    up_freq = 'up_freq'


class StrategyStockListTable(Base):
    __tablename__ = 'strategy_stock_list'
    id = Column('id', String, primary_key=True)
    strategy_code = Column('strategy_code', String)
    ticker = Column('ticker', String)
    rank = Column('rank', Integer)
    created_at = Column('created_at', DateTime)

    def __repr__(self):
        return f"{self.strategy_code} {self.ticker} {self.rank}"


def get_engine():
    return aistock_database.connect()


def get_strategy_stocks_to_list(strategy_code: str) -> list:
    s = retrieve_strategy_stocks(strategy_code)['ticker']
    return s.to_list()


def retrieve_strategy_stocks(strategy_code: str) -> DataFrame:
    select_stmt = select(StrategyStockListTable)
    stmt = select_stmt.where(
        StrategyStockListTable.strategy_code == strategy_code
    )
    df = pd.read_sql(stmt, db_session.bind)
    return df


def retrive_strategy_stocks_rank(code, limit=10) -> DataFrame:
    select_stmt = select(StrategyStockListTable)
    stmt = select_stmt.where(
        StrategyStockListTable.strategy_code == code
    )
    stmt.order_by(StrategyStockListTable.rank)
    df = pd.read_sql(stmt, db_session.bind)[:10]
    return df


def reset_all_rows():
    """
    모든 로우를 지움
    """
    db_session.query(StrategyStockListTable).delete()
    db_session.commit()


def count():
    db_session.query(StrategyStockListTable).count()
