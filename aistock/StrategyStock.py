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
    date = Column('date', DateTime)

    def __repr__(self):
        return f"{self.strategy_code} {self.ticker} {self.rank}"


def get_engine():
    return aistock_database.connect()

