"""
Created on: 12 Dec 2023
Script to populate the User database table to start writing data to it
"""
import json
import os
from typing import Dict

import pandas as pd
from sqlalchemy.exc import IntegrityError

from portfolio_tracker import db, create_app
from portfolio_tracker.models.models import User, Stock, SecurityPrices
from portfolio_tracker.utils.return_paths import get_project_dir
from portfolio_tracker.scripts.price_scraping import download_stock_data
from portfolio_tracker.utils.data_cleaning import prep_stock_data_for_table


app = create_app()


def insert_prices_into_db(
        stock_data_dict: Dict[str, pd.DataFrame],
        start_date: str,
        end_date: str
) -> None:
    with app.app_context():
        # populate the database
        for ticker, data in stock_data_dict.items():
            # query stock ID based on ticker
            stock = db.session.query(Stock).filter_by(ticker=ticker).first()
            if stock is None:
                print(f"Stock with ticker {ticker} isn't found")
                continue  # skip if the ticker isn't found in the database

            for index, row in data.iterrows():
                if start_date <= row['date'] <= end_date:
                    # Check if the price for that date already exists to avoid duplicates
                    exists = db.session.query(SecurityPrices).filter_by(stock_id=stock.id, date=row['date']).first()

                if not exists:
                    price_record = SecurityPrices(
                        stock_id=stock.id,
                        date=row['date'],
                        close_price=row['price']
                    )
                    db.session.add(price_record)

                    print(f"Price for {ticker} on {row['date']} already exists.")
                    continue  # Skip this iteration

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        print("IntegrityError: Possible duplicate entry found.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while inserting stock prices: {e}")
    finally:
        db.session.close()

    print("The database has been populated with the required data")


def fetch_and_insert_stock_data(
    date_start: str,
    date_end: str
):
    json_path = os.path.join(get_project_dir(), 'portfolio_tracker', 'config', 'stocks.json')
    with open(json_path) as file:
        stocks_dict = json.load(file)

        stock_tickers_lst = [tckr['ticker'] for tckr in stocks_dict]

        stock_price_df = download_stock_data(
            stock_list=stock_tickers_lst,
            date_start=date_start,
            date_end=date_end
        )

        stock_price_clean_df = prep_stock_data_for_table(raw_stock_df=stock_price_df)

        stock_price_dct = {stck: stock_price_clean_df.loc[stock_price_clean_df['stock'] == stck].copy()
                           for stck in stock_price_clean_df['stock'].unique()}

        insert_prices_into_db(stock_data_dict=stock_price_dct,
                              start_date=date_start,
                              end_date=date_end)


if __name__ == '__main__':
    date_start = '2010-01-01'
    date_end = '2023-12-31'
    fetch_and_insert_stock_data(
        date_start=date_start,
        date_end=date_end
    )
