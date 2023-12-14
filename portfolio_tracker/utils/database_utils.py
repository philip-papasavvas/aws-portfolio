
"""
Created on: 12 Dec 2023
Script to populate the User database table to start writing data to it
"""
import os
import json
from typing import Dict

import pandas as pd
from sqlalchemy.exc import IntegrityError

from portfolio_tracker import db, create_app
from portfolio_tracker.models.models import User, Stock

app = create_app()


def insert_prices_into_db(stock_data_dict: Dict[str, pd.DataFrame]) -> None:
    from flask import current_app
    json_path = os.path.join(current_app.root_path, 'config', 'stocks.json')
    pass


if __name__ == '__main__':
    import datetime

    from portfolio_tracker.utils.return_paths import get_project_dir
    from portfolio_tracker.scripts.price_scraping import download_stock_data
    from portfolio_tracker.utils.data_cleaning import prep_stock_data_for_table

    with open(os.path.join(get_project_dir(), 'portfolio_tracker', 'config', 'stocks.json')) as file:
        stocks_dict = json.load(file)
    stock_tickers_lst = [tckr['ticker'] for tckr in stocks_dict]
    date_yesterday = datetime.datetime.now().strftime("%Y-%m-%d")

    stock_price_df = download_stock_data(
        stock_list=stock_tickers_lst,
        date_start='2023-01-01',
        date_end=date_yesterday
    )
    stock_price_clean_df = prep_stock_data_for_table(raw_stock_df=stock_price_df)

    # get it in the format of a dictionary with keys and values
    unique_stocks = stock_price_clean_df['stock'].unique()
    stock_price_dct = {}
    for stck in unique_stocks:
        stock_price_dct[stck] = stock_price_clean_df.loc[stock_price_clean_df['stock'] == stck].copy()

    from portfolio_tracker.models.models import Stock, SecurityPrices

    with app.app_context():
        # populate the database
        for ticker, data in stock_price_dct.items():
            # query stock ID based on ticker
            stock = db.session.query(Stock).filter_by(ticker=ticker).first()
            if stock is None:
                print(f"Stock with ticker {ticker} isn't found")
                continue # skip if the ticker isn't found in the database

            for index, row in data.iterrows():
                date = row['date']
                # Check if the price for that date already exists to avoid duplicates
                exists = db.session.query(SecurityPrices).filter_by(stock_id=stock.id, date=date).first()
                if exists:
                    print(f"Price for {ticker} on {date} already exists.")
                    continue  # Skip this iteration

                    # Create and add the new SecurityPrices entry
                price_record = SecurityPrices(
                    stock_id=stock.id,
                    date=date,
                    close_price=row['price']
                )
                db.session.add(price_record)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred while inserting stock prices: {e}")
        finally:
            db.session.close()

        print("The database has been populated with the required data")
