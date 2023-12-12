"""
Created on: 20 Nov 2023
Created by: Philip P

Script for scraping yfinance for US security prices & another source for mutual fund prices
"""
import datetime
from typing import Dict

# third party imports
import numpy as np
import pandas as pd
import yfinance


def increment_date_by_day(
    date_in: str,
    is_reverse: bool = True
) -> str:
    """
    Helper function to increment (back or forward) a date in time, expected format YYYY-MM-DD.
    By default, it will go back in time one increment
    """
    date_dt = datetime.datetime.strptime(date_in, '%Y-%m-%d')
    sign = 1 if is_reverse else -1
    date_out = date_dt - datetime.timedelta(days=sign * 1)

    return str(date_out)


def return_tickers_purchase_dict(
    ticker_purchase_dct: Dict[str, str]
) -> Dict[str, dict]:
    """
    Function to return the purchase price of stock tickers according to the input dictionary
    fed in. This function will catch an error if there is no price returned/if the dataframe
    is empty
    """

    ticker_purchase_price_dct = {}
    for stock, dt in ticker_purchase_dct.items():
        purchase_date = ticker_purchase_dct[stock]
        ticker_px = yfinance.download(
            tickers=stock,
            start=increment_date_by_day(date_in=purchase_date, is_reverse=True),
            end=purchase_date
        )
        if not ticker_px.empty:
            ticker_purchase_price_dct[stock] = ticker_px['Adj Close'].iloc[0]
        else:
            ticker_purchase_price_dct[stock] = 'n/a'

    # put the dictionaries together to give the purchase date and purchase price
    combined_stock_px_dct = {}
    for stock, purchase_px in ticker_purchase_price_dct.items():
        combined_stock_px_dct[stock] = {
            'date': None,
            'price': None
        }

    # first fill the dates
    for stock, date in ticker_purchase_dict.items():
        combined_stock_px_dct[stock]['date'] = ticker_purchase_dict[stock]

    # now fill the prices
    for stock, date in ticker_purchase_price_dct.items():
        combined_stock_px_dct[stock]['price'] = ticker_purchase_price_dct[stock]

    return combined_stock_px_dct


if __name__ == '__main__':
    date_yesterday = datetime.datetime.now().strftime("%Y-%m-%d")

    # portfolio stocks
    stock_tickers = ['TSLA', 'MSFT', 'BRK-B', 'NVDA', 'GOOGL']

    # get the last day's prices
    last_day_px = yfinance.download(
        tickers=stock_tickers,
        start=date_yesterday,
        end=date_yesterday
    )

    # unstack the pd dataframe
    price_df_full = last_day_px.unstack().reset_index()
    price_df_full.columns = ['measure', 'stock', 'date', 'price']

    # keep only the adjusted close price
    price_df = price_df_full.loc[price_df_full['measure'] == 'Adj Close'].copy()

    # now map the opening prices for each stock too - define a dictionary of the
    # ticker and the day it way purchased
    ticker_purchase_dict = {
        'MSFT': '2023-10-30',
        'TSLA': '2023-05-26',
        'BRK-B': '2023-05-31',
        'AMZN': '2023-04-18',
        'NVDA': '2023-04-12',
        'GOOGL': '2023-11-10'
    }

    ticker_result_dct = return_tickers_purchase_dict(
        ticker_purchase_dct=ticker_purchase_dict
    )