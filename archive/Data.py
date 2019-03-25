# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 16:15:31 2018

API Key: pbyCSveaZa6eST4WxX7y
@author: Caelum Kamps
"""

import quandl
quandl.ApiConfig.api_key = 'pbyCSveaZa6eST4WxX7y'

# get the table for daily stock prices and,
# filter the table for selected tickers, columns within a time range
# set paginate to True because Quandl limits tables API to 10,000 rows per call

data = quandl.get_table('WIKI/PRICES', ticker = ['AAPL', 'MSFT', 'WMT'], 
                        qopts = { 'columns': ['ticker', 'date', 'adj_close'] }, 
                        date = { 'gte': '2017-12-31', 'lte': '2018-12-31' }, 
                        paginate=True)



# create a new dataframe with 'date' column as index
new = data.set_index('date')

# use pandas pivot function to sort adj_close by tickers
clean_data = new.pivot(columns='ticker')


