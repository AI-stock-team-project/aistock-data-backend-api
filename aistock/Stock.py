from sqlalchemy import Column, Integer, String

import aistock.database as aistock_database
from aistock.database import Base


class StockTable(Base):
    """
    sqlalchemy의 ORM 을 이용하기 위한 모델
    """
    __tablename__ = 'stock'
    id = Column('id', String, primary_key=True)
    code = Column('code', String)
    code_isin = Column('code_isin', String)
    symbol = Column('symbol', Integer)
    name = Column('name', Integer)
    market = Column('market', Integer)
    is_active = Column('is_active', String)

    def __repr__(self):
        return f"{self.id} {self.name} {self.code} {self.code_isin} {self.symbol}"


def get_engine():
    return aistock_database.connect()
