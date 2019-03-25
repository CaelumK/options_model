# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 13:26:57 2018

@author: Caelum.kamps
"""

import security_objects as so
import plotting as p
 
# Equity Object - Used as the underlying for options
'''
init (self, tckr, current_price, dividend, 
      historical_volatility, price_paid, number_of_shares)
'''
tsla = so.equity('TSLA', 268.80, 0, 0, 0, 0)

# Speficy option objects
'''
init (self, underlying, option_type, option_position, strike, 
                 implied_volatility, days_to_expiration, trading_days, 
                 price_paid, number_of_contracts, interest_rate = rate, 
                 commission = commission, fixed_commission = fixed_commission):
'''
tsla_p = so.option(tsla, 'put','long', 200, .6945, 303, 365, 26.45, 1)
tsla_p2 = so.option(tsla, 'put','short',200, .7149, 184, 365, 18.2, 1)


# Create a portfolio of options held
book = [tsla_p, tsla_p2]

p.plot_time_independent(book, step = 3)
p.plot_bleed(book, attribute = 'value', step = 4, number_of_intervals = 4)

#p.plot_hedge(book, step = 1, fdo = 0/252, plot_components = .2)
