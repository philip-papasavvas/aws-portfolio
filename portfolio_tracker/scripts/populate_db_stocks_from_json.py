"""
Created on: 12 Dec 2023
Script to populate the Stock database table with stock data from a JSON file
"""
import os
import json
from sqlalchemy.exc import IntegrityError
from flask import current_app

from portfolio_tracker import create_app
from portfolio_tracker.models.models import Stock, db

app = create_app()


def populate_stocks_db_table():
    """
    Reads stock data from a JSON file and populate the Stock table in the database. The function looks for
    a 'stocks.json' file in the 'config' directory relative to the current application's root path.
    It expects the JSON file to contain a list of dictionaries, each with 'ticker' and 'name'
    keys corresponding to the stock's ticker symbol and full name. Each stock from the JSON file is
    added to the database session and committed to the Stock table. If an IntegrityError occurs during
    commit, the transaction is rolled back.
    """
    json_path = os.path.join(current_app.root_path, 'config', 'stocks.json')
    with open(json_path, 'r') as file:
        stock_list = json.load(file)

    for stock_info in stock_list:
        stock = Stock(ticker=stock_info['ticker'], name=stock_info['name'])
        db.session.add(stock)

    try:
        db.session.commit() # commit the session to the database
    except IntegrityError:
        db.session.rollback() # rollback the transaction if an error occurs


if __name__ == '__main__':
    with app.app_context():
        # populate the database
        populate_stocks_db_table()
        print("The database table 'stocks' has been populated with the stock data")
