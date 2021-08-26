import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import sqlite3


def create_engine():
    """
    환경변수로 설정된 값을 토대로 커넥션을 위한 engine 설정을 완료한다.
    :return: sqlalchemy engine
    """
    database_host = os.getenv('DB_HOST', 'localhost')
    database_port = os.getenv('DB_PORT', '3306')
    database_name = os.getenv('DB_DATABASE', 'default')
    database_username = os.getenv('DB_USER', 'default')
    database_password = os.getenv('DB_PASSWORD', '')
    _engine = sqlalchemy.create_engine(
        'mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}'.format(
            database_username, database_password,
            database_host, database_port, database_name))
    return _engine


def connect():
    """
    환경변수로 설정된 값을 토대로 커넥션을 위한 engine 설정을 완료한다.
    :return: sqlalchemy engine
    """
    database_host = os.getenv('DB_HOST', 'localhost')
    database_port = os.getenv('DB_PORT', '3306')
    database_name = os.getenv('DB_DATABASE', 'default')
    database_username = os.getenv('DB_USER', 'default')
    database_password = os.getenv('DB_PASSWORD', '')
    _engine = sqlalchemy.create_engine(
        'mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}'.format(
            database_username, database_password,
            database_host, database_port, database_name))
    return _engine


def connect_local():
    """
    환경 변수 설정이 없을 때에는 sqlite에 저장하게 함. 테스트용도나 로컬 용도
    환경 변수 설정이 되어있으면, 설정된 데이터베이스에 연결
    :return: sqlalchemy engine
    """
    if os.getenv('DB_HOST', None) is None:
        # 데이터베이스가 설정되어 있지 않으면 sqlite 로 테스트.
        return sqlite3.connect('test2.db')
    else:
        return connect()


engine = create_engine()
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
