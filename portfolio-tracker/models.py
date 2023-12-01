# Added on Thursday 30 Nov 2023 to add the db schema

# third party imports
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Model, String, Float, Boolean, DateTime, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Stock(db.Model):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    ticker = Column(String(10), unique=True, nullable=False)
    name = Column(String(64), nullable=False)

class Transactions(db.Model):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id')) # add in foreign key
    stock_id = Column(Integer, ForeignKey('stocks.id')) # add in foreign key
    transaction_type = Column(Boolean, nullable=False)
    quantity_shares = Column(Integer, nullable=False)
    date_transaction = Column(DateTime, nullable=False)

class Portfolio(db.Model):
    __tablename__ = 'portfolio'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id')) # add in foreign key
    stock_id = Column(Integer, ForeignKey('stocks.id'))
    total_shares = Column(Integer, nullable=False)


class SecurityPrices(db.Model):
    __tablename__ = 'security_prices'

    price_id = Column(Integer, primary_key=True)
    stock_id = Column(Integer, ForeignKey('stocks.id'))
    date = Column(DateTime, nullable=False)
    close_price = Column(Float, nullable=False)
