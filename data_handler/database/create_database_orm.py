from os.path import dirname, join

from sqlalchemy import create_engine, Column, Integer, String, Sequence, Float, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.sql import *
import os


BASEDIR = dirname(dirname(__file__))


def connect_db(database="new_esg_paper_trading.db"):
    db = create_engine('sqlite:///' + join(BASEDIR, database))
    return db


def create_tables():
    engine = connect_db()
    from src.trading.paper.data.models.esg_returns import StandardPortfolioReturns, StandardStrategyContributions, \
        EsgPortfolioReturns, EsgStrategyContributions, LivePortfolioReturns

    StandardPortfolioReturns.__table__.create(bind=engine, checkfirst=True)
    StandardStrategyContributions.__table__.create(bind=engine, checkfirst=True)
    EsgPortfolioReturns.__table__.create(bind=engine, checkfirst=True)
    EsgStrategyContributions.__table__.create(bind=engine, checkfirst=True)
    LivePortfolioReturns.__table__.create(bind=engine, checkfirst=True)


if __name__ == '__main__':
    create_tables()
