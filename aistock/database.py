import sqlalchemy
import os


def get_engine():
    database_host = os.getenv('DB_HOST', 'localhost')
    database_port = os.getenv('DB_PORT', '3306')
    database_name = os.getenv('DB_DATABASE', 'default')
    database_username = os.getenv('DB_USER', 'default')
    database_password = os.getenv('DB_PASSWORD', '')
    engine = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}'.
                                      format(database_username, database_password,
                                             database_host, database_port, database_name))
    return engine
