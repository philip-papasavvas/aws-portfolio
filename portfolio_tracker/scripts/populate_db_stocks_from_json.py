"""
Created on: 12 Dec 2023
Script to populate the Stock database table with stock data from a JSON file
"""
import os
import json
from typing import Dict

from sqlalchemy.exc import IntegrityError
from flask import current_app
import psycopg2

from portfolio_tracker import create_app
from portfolio_tracker.models.models import Stock, db
from portfolio_tracker.utils.return_paths import get_project_dir

app = create_app()
with open(os.path.join(get_project_dir(), 'portfolio_tracker', 'config', 'credentials.JSON')) as file:
    credentials = json.load(file)


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
        db.session.commit()  # commit the session to the database
    except IntegrityError:
        db.session.rollback()  # rollback the transaction if an error occurs


def populate_stocks_db_table_aws(credentials: Dict[str, str]):
    """
    Populate the 'stocks' table in the PostgreSQL database with stock data.

    Connects to the database using credentials dictionary, reads stock data from
    a JSON file, and inserts it into the 'stocks' table. Assumes the presence
    of 'credentials' with necessary keys and 'stocks.json' in the specified
    directory structure.

    Args:
        credentials: A dictionary with keys 'db-name', 'username', 'password', and 'host'.

    Raises:
        psycopg2.DatabaseError: If issues occur with database operations.
        FileNotFoundError: If the 'stocks.json' file is not found.
        KeyError: If essential keys are missing in the 'credentials' or stock entries.
    """
    conn = psycopg2.connect(
        dbname=credentials['db-name'],
        user=credentials['username'],
        password=credentials['password'],
        host=credentials['host']
    )
    cursor = conn.cursor()

    json_path = os.path.join(get_project_dir(), 'portfolio_tracker', 'config', 'stocks.json')
    with open(json_path, 'r') as file_stocks:
        stock_list = json.load(file_stocks)

    for stock in stock_list:
        ticker = stock['ticker']
        company_name = stock['name']
        cursor.execute(
            "INSERT INTO stocks (ticker_symbol, company_name) VALUES (%s, %s)",
            (ticker, company_name)
        )

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Updated the {credentials['db-name']} table in the DB. Check this"
          f"using PostgreSQL client, such as pgAdmin")


if __name__ == '__main__':
    # with app.app_context():
    #     # populate the database
    #     populate_stocks_db_table()
    #     print("The database table 'stocks' has been populated with the stock data")

    populate_stocks_db_table_aws()
