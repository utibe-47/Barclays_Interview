from os.path import dirname, join

from data_handler.database import db, Base
from data_handler.database.models.historical_prices import InstrumentPrices

BASEDIR = dirname(dirname(__file__))


def database_connection(database):
    engine = db.create_engine('sqlite:///' + join(BASEDIR, database))
    conn = engine.connect()
    return conn, engine


def create_tables(database_name='barclays_interview.db'):
    conn, engine = database_connection(database_name)
    if not engine.dialect.has_table(engine, 'InstrumentPrices'):
        Base.metadata.create_all(engine, checkfirst=True)


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        print(e)


def drop_tables(database_name='barclays_interview.db'):
    conn, engine = database_connection(database_name)
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    create_tables()
