import pandas as pd
import pandas_datareader.data as web
from datetime import datetime, timedelta, date
from typing import List
import logging
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


class PortfolioBuilder:
    """

    """
    def __init__(self):
        self.tickers_list = []
        self.amount_of_stocks = 0
        self.my_df = []
        self.my_portfolio = []
        self.x_t = []
        self.total_x_t = []

    def get_daily_data(self, tickers_list: List[str],
                       start_date: date,
                       end_date: date = date.today()
                       ) -> pd.DataFrame:
        """
        get stock tickers adj_close price for specified dates.

        :param List[str] tickers_list: stock tickers names as a list of strings.
        :param date start_date: first date for query
        :param date end_date: optional, last date for query, if not used assumes today
        :return: daily adjusted close price data as a pandas DataFrame
        :rtype: pd.DataFrame

        """
        self.tickers_list = tickers_list
        self.amount_of_stocks = len(tickers_list)
        try:
            self.my_df = web.DataReader(self.tickers_list, start=start_date, end=end_date, data_source="yahoo")[
                'Adj Close']
            # my_df = my_df.reindex(my_df.mean().sort_values().index[::], axis="columns")
            # my_df.head()
        except ResourceWarning as e:
            logging.error(f'error getting stocks_api data', exc_info=True)
        else:
            self.my_df = self.my_df.reindex(self.my_df.mean().sort_values().index[::-1], axis="columns")
        return self.my_df


def print_chart(df):
    stocks_symbol_list = df.columns.values.tolist()

    fig = plt.figure(figsize=(10, 6))

    for i in stocks_symbol_list:
        plt.plot(df[i])
        plt.title("US real estate main stocks performance chart")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.xticks()
    plt.legend(stocks_symbol_list)
    plt.ion()
    plt.show()
    plt.pause(5)


# noinspection PyTypeChecker
def get_stocks_data(stocks_symbol_list, years):
    # creating the PortfolioBuilder class object
    pb = PortfolioBuilder()

    # calculating time difference
    from_date = (datetime.today() - timedelta(days=years * 365)).strftime("%Y-%m-%d")
    to_date = datetime.today()

    # getting the stocks data from the api
    df = pb.get_daily_data(stocks_symbol_list, from_date, to_date)

    return df


def main(years=5):
    stocks_symbol_list = ['VGSIX', 'FSRNX', 'IYR']
    stocks_df = get_stocks_data(stocks_symbol_list, years)
    print_chart(stocks_df)


if __name__ == '__main__':
    main()
