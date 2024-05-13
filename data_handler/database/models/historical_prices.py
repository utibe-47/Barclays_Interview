from datetime import datetime
from data_handler.database import db, Base


class InstrumentPrices(Base):
    __tablename__ = 'instrument_prices'
    Id = db.Column(db.Integer(), primary_key=True, unique=True)
    CobDate = db.Column(db.DateTime(timezone=False), nullable=False, default=datetime.now())
    Ticker = db.Column(db.String())
    Name = db.Column(db.String())
    Price = db.Column(db.Float(), default=0.0)
    Volume = db.Column(db.Float(), default=0.0)


header = ['Date', 'Ticker', 'Price', 'Volume']
header_csv = ['Date', 'Ticker', 'Price', 'Volume']
header_with_date = ['Date'] + header
header_csv_with_date = ['Date'] + header_csv
