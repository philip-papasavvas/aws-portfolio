"""
Created on: 20 Nov 2023
Created by: Philip P

Script for scraping yfinance for US security prices & another source for mutual fund prices
"""
import datetime
from typing import Dict, List, Union

import pandas as pd
import yfinance

from portfolio_tracker.utils.data_cleaning import prep_stock_data_for_table


def download_stock_data(
        stock_list: List[str],
        date_start: Union[str, datetime],
        date_end: Union[str, datetime]
):
    """
    Helper function to download stock data for multiple tickers and a date range.
    """
    raw_stocks_df = yfinance.download(
        tickers=stock_list,
        start=date_start,
        end=date_end,
        group_by='ticker',
        rounding=True  # rounds to two decimal places
    )

    return raw_stocks_df


def get_stock_prices_securities(
        stock_list: List[str],
        date_start: Union[str, datetime],
        date_end: Union[str, datetime],
        field: str = 'Adj Close'
) -> dict:
    """
    Function to get the securities' stock prices between the given start and end dates.
    """
    # Download stock data for all tickers in the list for the given date range
    stocks_data = download_stock_data(
        stock_list=stock_list,
        date_start=date_start,
        date_end=date_end,
    )

    stocks_df = {}
    for stock in stock_list:
        try:
            # Extract the Adjusted Close prices for the specific stock
            stocks_df[stock] = stocks_data[stock][field] if len(stock_list) > 1 else stocks_data[field]
        except KeyError:
            stocks_df[stock] = 'n/a'

    return stocks_df


def return_tickers_purchase_dict(
        ticker_purchase_dict: Dict[str, str],
        field: str = 'Adj Close'
) -> Dict[str, dict]:
    """
    Function to return the purchase price of stock tickers according to the input dictionary
    fed in. This function will catch an error if there is no price returned/if the dataframe
    is empty
    """
    combined_stock_px_dict = {}

    # Get a list of unique dates from the purchase dictionary to minimize the number of requests
    unique_dates = list(set(ticker_purchase_dict.values()))
    unique_dates.sort()

    # Download stock data for all unique dates
    stock_data = download_stock_data(
        stock_list=list(ticker_purchase_dict.keys()),
        date_start=unique_dates[0],
        date_end=unique_dates[-1]
    )

    # Extract the purchase price for each stock on its purchase date
    for stock, purchase_date in ticker_purchase_dict.items():
        try:
            if isinstance(stock_data, pd.DataFrame):  # Single ticker case
                price = stock_data.loc[purchase_date][field]
            else:  # Multiple tickers case
                price = stock_data[stock].loc[purchase_date][field]
        except KeyError:
            price = 'n/a'

        combined_stock_px_dict[stock] = {
            'date': purchase_date,
            'price': price
        }

    return combined_stock_px_dict


if __name__ == '__main__':
    # get the stocks from the portfolio
    import json
    import os

    date_yesterday = datetime.datetime.now().strftime("%Y-%m-%d")

    with open(os.path.join(os.getcwd(), 'portfolio_tracker', 'config', 'stocks.json')) as file:
        stocks_dict = json.load(file)
    stock_tickers_lst = [tckr['ticker'] for tckr in stocks_dict]

    stock_price_df = download_stock_data(
        stock_list=stock_tickers_lst,
        date_start='2023-01-01',
        date_end=date_yesterday
    )
    stock_price_clean_df = prep_stock_data_for_table(raw_stock_df=stock_price_df)

    # now map the opening prices for each stock too - define a dictionary of the
    # ticker and the day it way purchased
    ticker_purchase_dct = {
        'MSFT': '2023-10-30',
        'TSLA': '2023-05-26',
        'BRK-B': '2023-05-31',
        'AMZN': '2023-04-18',
        'NVDA': '2023-04-12',
        'GOOGL': '2023-11-10'
    }

    ticker_result_dct = return_tickers_purchase_dict(
        ticker_purchase_dict=ticker_purchase_dct
    )
