"""
Created on: 20 Nov 2023
Created by: Philip P

Script for scraping yfinance for US security prices & another source for mutual fund prices
"""
# third party imports
import numpy as np
import pandas as pd
import yfinance

if __name__ == '__main__':
    example_px = yfinance.download(
        tickers='MSFT',
        start='2023-11-16',
        end='2023-11-17'
    )

    # unstack the pd dataframe
    example_price_df = example_px.unstack().reset_index()
    example_price_df.columns = ['measure', 'date', 'price']

    # keep only the adjusted close price
    price_df = example_price_df.loc[example_price_df['measure'] == 'Adj Close'].copy()
    