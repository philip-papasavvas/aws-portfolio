"""
Created on: 2 January 2024
Script to inspect current database and determine gaps/update steps required
"""
import sqlite3
from sqlite3 import Error, Connection


def create_connection(db_file_path: str) -> Connection:
    """
    Create a DB connection to the sqlite db specified by the db_file_path given

    Returns:
        Connection: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file_path)
        return conn
    except Error as e:
        print(e)
    return conn


def run_sql(conn: Connection, sql_str: str):
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
    conn = create_connection(database_path)

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
