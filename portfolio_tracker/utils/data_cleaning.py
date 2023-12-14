import datetime

import pandas as pd


def increment_date_by_day(
    date_in: str,
    is_reverse: bool = True
) -> str:
    """
    Helper function to increment (back or forward) a date in time, expected format YYYY-MM-DD.
    By default, it will go back in time one increment
    """
    date_dt = datetime.datetime.strptime(date_in, '%Y-%m-%d')
    sign = -1 if is_reverse else 1
    date_out = date_dt + datetime.timedelta(days=sign * 1)

    return str(date_out)


def prep_stock_data_for_table(
    raw_stock_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Docstring here
    """
    # unstack the dataframe
    price_df_full = raw_stock_df.unstack().reset_index()
    price_df_full.columns = ['measure', 'stock', 'date', 'price']

    # keep only the adjusted close price
    price_df = price_df_full.loc[price_df_full['measure'] == 'Adj Close'].copy()

    return price_df


if __name__ == '__main__':
    pass
