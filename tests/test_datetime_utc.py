"""
MySQL 과 Flask, Python 에서 Datetime 에 대한 Timezone 과 관련된 테스트.
"""
# noinspection PyUnresolvedReferences
from deprecated import deprecated
# noinspection PyUnresolvedReferences
from datetime import timedelta, datetime, timezone
from dateutil import tz
import pytz
from aistock.util import c_dateutil

import pandas as pd
# noinspection PyUnresolvedReferences
from pandas import Series, DataFrame

from sqlalchemy import Column, Integer, String, select, DateTime, func
import aistock.database as aistock_database
from aistock.database import Base, db_session


class DateTimeUTCTestTable(Base):
    __tablename__ = 'temp_datetime_test'
    id = Column('id', Integer, primary_key=True)
    text = Column('text', String(255))
    # created_at = Column('date', DateTime(timezone=True), default=datetime.utcnow)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"{self.id} {self.text} {self.created_at}"


def get_engine():
    return aistock_database.connect()


def test():
    # create()
    query = db_session.query(DateTimeUTCTestTable)[0]

    # print(query.created_at)
    created_at = query.created_at
    print(type(created_at))
    print(created_at)

    # print(c_dateutil.test_utc_to_local(created_at))
    print(c_dateutil.utc_to_local(created_at).strftime('%Y-%m-%d %H:%M:%S %Z%z'))

    # UTC 타임인걸 지정.
    # created_at = created_at.replace(tzinfo=timezone.utc)
    # print(created_at.strftime('%Y-%m-%d %H:%M:%S %Z%z'))

    # dateutil 을 사용한 방법
    # kst_dt = created_at.astimezone(tz.tzlocal())
    # print(kst_dt.strftime('%Y-%m-%d %H:%M:%S %Z%z'))

    # for q in query:
    #    # print(q)
    #    print(type(q.created_at))
    #    dd = q.created_at


def test_utc_to_local(dt: DateTime):
    # UTC 타임이라고 지정
    dt = dt.replace(tzinfo=timezone.utc)
    # print(dt.strftime('%Y-%m-%d %H:%M:%S %Z%z'))

    # dateutil 을 사용한 방법
    rv = dt.astimezone(tz.tzlocal())
    # print(rv.strftime('%Y-%m-%d %H:%M:%S %Z%z'))
    return rv


def test_utc_to_kst_pytz(dt: DateTime):
    kst = pytz.timezone('Asia/Seoul')
    utc = pytz.timezone('UTC')

    # UTC 타임이라고 지정
    d = utc.localize(dt)
    
    # kst로 시간 변경
    rv = d.astimezone(kst)
    # print(rv.strftime('%Y-%m-%d %H:%M:%S %Z%z'))
    return rv


def create():
    # 테이블 생성
    DateTimeUTCTestTable.__table__.create(bind=get_engine(), checkfirst=True)

    a1 = DateTimeUTCTestTable(id=1, text='abcd')
    a2 = DateTimeUTCTestTable(id=2, text='efgh')

    db_session.add(a1)
    db_session.add(a2)
    db_session.commit()
    # db_session.


if __name__ == '__main__':
    test()
