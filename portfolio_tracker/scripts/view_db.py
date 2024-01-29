"""
Created on: 2 January 2024
Script to inspect current database and determine gaps/update steps required
"""
import json
import os

import psycopg2
from psycopg2.extensions import connection

from portfolio_tracker.utils.return_paths import get_project_dir

with open(os.path.join(get_project_dir(), 'portfolio_tracker', 'config', 'credentials.JSON')) as file:
    credentials = json.load(file)

conn = psycopg2.connect(
        dbname=credentials['db-name'],
        user=credentials['username'],
        password=credentials['password'],
        host=credentials['host']
)


def run_sql(conn: connection, sql_str: str):
    """
    Run SQL command and return the results
    """
    cur = conn.cursor()
    cur.execute(sql_str)
    rows = cur.fetchall()
    return rows


if __name__ == '__main__':
    import os
    from portfolio_tracker.utils.return_paths import get_project_dir

    database_path = os.path.join(get_project_dir(), 'instance', 'app.db')

    result = run_sql(
        conn=conn,
        sql_str="SELECT * FROM stocks"
    )
    # table names = users, stocks, transactions, portfolio, security_prices

    # stocks list
    stocks_list = [
        (1, 'TSLA', 'Tesla'),
        (2, 'MSFT', 'Microsoft'),
        (3, 'BRK-B', 'Berkshire Hathaway'),
        (4, 'NVDA', 'Nvidia'),
        (5, 'GOOGL', 'Alphabet'),
        (6, 'AMZN', 'Amazon')
    ]

    stocks_dict = {
        stock[0]: {
            'ticker': stock[1],
            'name': stock[2]
        }
        for stock in stocks_list
    }

    from pprint import pprint
    pprint(stocks_dict)
