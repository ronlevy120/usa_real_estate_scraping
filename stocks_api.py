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
    def __init__(self, years=5):
        self.tickers_list = []
        self.amount_of_stocks = 0
        self.my_df = []
        self.years = years
        self.stocks_symbol_list = ['FSRNX', 'IYR', 'USRT', 'XLRE', 'REET', 'VNQ', 'RWR']

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
        except ResourceWarning:
            logging.error(f'error getting stocks_api data', exc_info=True)
        else:
            self.my_df = self.my_df.reindex(self.my_df.mean().sort_values().index[::-1], axis="columns")
        return self.my_df

    def print_chart(self):
        df = self.get_stocks_data()
        plt.figure(figsize=(10, 6))

        for i in self.stocks_symbol_list:
            plt.plot(df[i])
            plt.title("US real estate main stocks performance chart")
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.xticks()
        plt.legend(self.stocks_symbol_list)
        plt.ion()
        plt.show()
        plt.pause(5)

    def get_stocks_data(self):
        # calculating time difference
        self.from_date = (datetime.today() - timedelta(days=self.years * 365)).strftime("%Y-%m-%d")
        self.to_date = datetime.today()

        # getting the stocks data from the api
        df = self.get_daily_data(self.stocks_symbol_list, self.from_date, self.to_date)

        return df

    def average_yield(self):
        df = self.get_stocks_data()
        avg_yield = round(df.apply(lambda x: x.iloc[-1] / x.iloc[0] * 100 - 100)[1].mean(), 3)
        return avg_yield, self.stocks_symbol_list, self.from_date, self.to_date

