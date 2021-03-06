"""
Purpose:
The following module is the DataGenerator. It is responsible for
downloading the Coronavirus data and the Goolge Trends data
for the given parameters. Data is output as two dataframes.

Date: 5/31/2020

Author: Tara Wilson
"""

from datetime import datetime, timedelta
import pandas as pd
import us
from pytrends.request import TrendReq

class DataGenerator:
    """
    The DataGenerator class is used to download the data from its sources
    and pass it to the DataProcessor. It has the following attributes:

    state: the state for which the Coronavirus and Google Trends data is gathered
    keywords: the keyword(s) for which the the Google Trends data is gathered
    days: the number of days for which the data should be aggregated for
        (optional - default value is one year)
    """
    def __init__(self, state, keywords, days=366):
        self.state = state
        self.keywords = keywords
        self.days = days
        self.covid_data = None
        self.trend_data = None

    def run(self):
        """
        Calls for the data to be aggregated.
        """
        self.get_data()

    def get_data(self):
        """
        Gathers coronavirus data for a given state from the Bing Coronavirus
        data source as well as Google Trends data from the last year for
        the given keywords.
        Inputs:
            - state: Full name of state for which to gather the data
            - keywords: List of keywords to gather Google Trends data for
        Outputs:
            - covid_data: A dataframe with coronavirus counts of confirmed cases,
            deaths, and recoveries for the given state
            - trend_data: A dataframe with Google Trends data for the given
            keywords and state over the past year, aggregated weekly
        """
        state_abbr = us.states.lookup(self.state).abbr
        domain = "https://raw.githubusercontent.com/microsoft"
        covid_project = "/Bing-COVID-19-Data/master/data/Bing-COVID19-Data.csv"
        url = domain + covid_project
        state_data = pd.read_csv(url)
        covid_data = state_data[(state_data.AdminRegion1 == self.state) &
                                (state_data.AdminRegion2.isnull())]
        end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=self.days)).strftime("%Y-%m-%d")
        user_timeframe = start_date + " " + end_date
        area_code = "en-US-" + state_abbr
        pytrend = TrendReq(hl=area_code, tz=480)
        pytrend.build_payload(kw_list=self.keywords, timeframe=user_timeframe)
        trend_data = pytrend.interest_over_time()
        self.covid_data = covid_data
        self.trend_data = trend_data
