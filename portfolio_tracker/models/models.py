"""
Created on: 30 Nov 2023
Add the db schema
"""

# third party imports
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    """
    The User model represents a registered user.

    Attributes:
        id: A unique integer identifying the user.
        username: The user's username.
        email: The user's email address.
        password_hash: The hashed version of the user's password.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Stock(db.Model):
    """
    The Stock model represents a stock in the database.

    Attributes:
        id: A unique integer identifying the stock.
        ticker: The stock's ticker symbol. This field is unique and cannot be null.
        name: The name of the stock. This field cannot be null.
    """
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    ticker = Column(String(10), unique=True, nullable=False)
    name = Column(String(64), nullable=False)


class Transactions(db.Model):
    """
    The Transactions model represents a stock transaction made by a user.

    Attributes:
        id: A unique integer identifying the transaction.
        user_id: An integer referencing the ID of the user who made the transaction.
        stock_id: An integer referencing the ID of the stock involved in the transaction.
        transaction_type: A boolean indicating the type of transaction. True represents a buy transaction,
                          False represents a sell transaction.
        quantity_shares: The number of shares involved in the transaction. This is a floating-point number
                         to accommodate fractional shares.
        date_transaction: The date and time when the transaction occurred.
    """

    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # add in foreign key
    stock_id = Column(Integer, ForeignKey('stocks.id'))  # add in foreign key
    is_purchase = Column(Boolean, nullable=False)
    quantity_shares = Column(Float, nullable=False)
    date_transaction = Column(DateTime, nullable=False)


class Portfolio(db.Model):
    """
    The Portfolio model represents the holdings of a user in a specific stock.

    Attributes:
        id: A unique integer identifying the portfolio entry.
        user_id: An integer referencing the ID of the user who owns the portfolio.
        stock_id: An integer referencing the ID of the stock in the portfolio.
        total_shares: The total number of shares the user holds in the referenced stock. This is a
                      floating-point number to accommodate fractional shares.
    """
    __tablename__ = 'portfolio'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # add in foreign key
    stock_id = Column(Integer, ForeignKey('stocks.id'))
    total_shares = Column(Float, nullable=False)


class SecurityPrices(db.Model):
    """
    The SecurityPrices model represents the closing prices of a stock on different dates.

    Attributes:
        price_id: A unique integer identifying the price entry.
        stock_id: An integer referencing the ID of the stock.
        date: The date when the specific closing price was recorded.
        close_price: The closing price of the referenced stock on the specified date.
    """
    __tablename__ = 'security_prices'

    price_id = Column(Integer, primary_key=True)
    stock_id = Column(Integer, ForeignKey('stocks.id'))
    date = Column(DateTime, nullable=False)
    close_price = Column(Float, nullable=False)

    def __repr__(self):
        return f"<SecurityPrice {self.stock_id} on {self.date}"
