from datetime import datetime
from sqlalchemy import desc, func, and_
from data_handler.database.models.thinkfolio_position import ThinkfolioPositions


def query_by_date(session, reason_code, date_limit=None):

    latest_date = session.query(ThinkfolioPositions.Date, ThinkfolioPositions.ReasonCode).filter(
        ThinkfolioPositions.ReasonCode == reason_code).distinct(
        ThinkfolioPositions.Date).order_by(desc('Date')).all()

    if date_limit is None:
        return latest_date
    else:
        latest_date = list(filter(lambda x: x[0] <= datetime.strptime(date_limit, '%Y/%m/%d'), latest_date))
    return latest_date


def query_data(session, reason_code, date=None):
    if date is None:
        date_limit = func.max(ThinkfolioPositions.Date)
        latest_orders = session.query(ThinkfolioPositions.Date, ThinkfolioPositions.Account,
                                      ThinkfolioPositions.Strategy, ThinkfolioPositions.ReasonCode).group_by(
            ThinkfolioPositions.Account, ThinkfolioPositions.Strategy,
            ThinkfolioPositions.ReasonCode).having(
            and_(ThinkfolioPositions.ReasonCode == reason_code, ThinkfolioPositions.Date == date_limit)).subquery()
    else:
        max_date = func.max(ThinkfolioPositions.Date)
        latest_orders = session.query(ThinkfolioPositions.Date, ThinkfolioPositions.Account,
                                      ThinkfolioPositions.Strategy, ThinkfolioPositions.ReasonCode).filter(
            ThinkfolioPositions.Date <= date).group_by(
            ThinkfolioPositions.Account, ThinkfolioPositions.Strategy,
            ThinkfolioPositions.ReasonCode).having(
            and_(ThinkfolioPositions.ReasonCode == reason_code, ThinkfolioPositions.Date == max_date)).subquery()

    data = session.query(ThinkfolioPositions).join(latest_orders, and_(
        ThinkfolioPositions.Strategy == latest_orders.c.Strategy,
        ThinkfolioPositions.Account == latest_orders.c.Account,
        ThinkfolioPositions.ReasonCode == latest_orders.c.ReasonCode,
        ThinkfolioPositions.Date == latest_orders.c.Date)).order_by(
        latest_orders.c.Date.desc(), ThinkfolioPositions.Date.desc()).all()

    return data


def query_latest_data(session, date_limit=None):

    if date_limit is None:
        latest_orders = session.query(ThinkfolioPositions.Date, ThinkfolioPositions.Account,
                                      ThinkfolioPositions.Strategy).group_by(
            ThinkfolioPositions.Account, ThinkfolioPositions.Strategy).having(
            ThinkfolioPositions.Date == func.max(ThinkfolioPositions.Date)).subquery()
    else:
        latest_orders = session.query(ThinkfolioPositions.Date, ThinkfolioPositions.Account,
                                      ThinkfolioPositions.Strategy).filter(
            ThinkfolioPositions.Date <= date_limit).group_by(
            ThinkfolioPositions.Account, ThinkfolioPositions.Strategy).having(
            ThinkfolioPositions.Date == func.max(ThinkfolioPositions.Date)).subquery()

    data = session.query(ThinkfolioPositions).join(latest_orders, and_(
        ThinkfolioPositions.Strategy == latest_orders.c.Strategy,
        ThinkfolioPositions.Account == latest_orders.c.Account,
        ThinkfolioPositions.Date == latest_orders.c.Date)).order_by(
        latest_orders.c.Date.desc(), ThinkfolioPositions.Date.desc()).all()

    return data
