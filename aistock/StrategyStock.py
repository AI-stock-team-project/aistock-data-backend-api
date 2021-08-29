import pandas as pd
from pandas import Series, DataFrame
# noinspection PyUnresolvedReferences
from deprecated import deprecated
# noinspection PyUnresolvedReferences
from datetime import timedelta, datetime

from sqlalchemy import Column, Integer, String, select, DateTime
import aistock.database as aistock_database
from aistock.database import Base, db_session


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


def retrieve_strategy_stocks(strategy_code=''):
    select_stmt = select(StrategyStockListTable)
    stmt = select_stmt.where(
        StrategyStockListTable.strategy_code == strategy_code
    )
    df = pd.read_sql(stmt, db_session.bind)
    return df
