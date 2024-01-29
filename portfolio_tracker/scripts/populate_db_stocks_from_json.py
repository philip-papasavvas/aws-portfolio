"""
Created on: 12 Dec 2023
Script to populate the Stock database table with stock data from a JSON file
"""
import json
import os
from typing import Dict

import psycopg2

from portfolio_tracker import create_app
from portfolio_tracker.utils.return_paths import get_project_dir

app = create_app()
with open(os.path.join(get_project_dir(), 'portfolio_tracker', 'config', 'credentials.JSON')) as file:
    credentials = json.load(file)


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
    populate_stocks_db_table_aws()
