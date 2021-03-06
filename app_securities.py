# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 18:11:00 2018

@author: Caelum Kamps
"""

from math import exp as e
from math import sqrt, log
from scipy.stats import norm
from datetime import datetime, timedelta



class equity:
    def __init__(self, tckr, current_price, dividend, historical_volatility, price_paid, number_of_shares):
        self.security = 'Stock'
        self.tckr = tckr
        self.shares = number_of_shares
        self.dividend = dividend
        self.hv = historical_volatility
        self.book_value = price_paid
        self.price = current_price
        
    def get_return(self, price):
        return (price - self.price)*self.shares
    
        
class option:
    rate = 0.0291
    commission = 0.025
    fixed_commission = 0.2
    
    # Greek Calculations
    def get_d1(self,S,K,r,d,iv,t):
        return (log(S/K) + (r - d + ((iv**2)/2))*t)/(iv*sqrt(t))
  
    def get_d2(self,d1,iv,t):
        return d1 - iv*sqrt(t)    
   
    def get_c_value(self,S,d,t,d1,K,r,d2):
        return S*e(-d*t)*norm.cdf(d1) - K*e(-r*t)*norm.cdf(d2)

    def get_p_value(self,S,d,t,d1,K,r,d2):
        return K*e(-r*t)*norm.cdf(-d2) - S*e(-d*t)*norm.cdf(-d1)

    def get_c_delta(self, d, t, d1):
        return e(-d*t)*norm.cdf(d1) 

    def get_p_delta(self,d,t,d1):
        return e(-d*t)*(norm.cdf(d1)-1)
    
    def get_gamma(self,d,d1,S,iv,t):
        return e(-d*t)*norm().pdf(d1)/(S*iv*sqrt(t))

    def get_vega(self,S,d,t,d1):
        return 0.01*S*e(-d*t)*sqrt(t)*norm.pdf(-d1)

    def get_c_theta(self,S,iv,d,d1,t,r,K,d2,days):
        return (1/days)*(-(S*iv*e(-d*t)*norm.pdf(-d1)/(2*sqrt(t))) - (r*K*e(-r*t)*norm.cdf(d2)) + (d*S*e(-d*t)*norm.cdf(d1)))

    def get_p_theta(self,S,iv,d,d1,t,r,K,d2,days):
        return (1/days)*(-(S*iv*e(-d*t)*norm.pdf(-d1)/(2*sqrt(t))) + (r*K*e(-r*t)*norm.cdf(-d2)) - (d*S*e(-d*t)*norm.cdf(-d1)))
    
    # Update all Greeks
    def update_greeks(self):
        self.d1 = self.get_d1(self.current_price, self.strike,self.rate,
                              self.dividend, self.iv, self.expt)
        
        self.d2 = self.get_d2(self.d1, self.iv, self.expt)
        
        if self.option_type == 'call':
            self.t_value = self.get_c_value(self.current_price, self.dividend,
                                            self.expt, self.d1, self.strike,
                                            self.rate, self.d2)
            
            self.delta = self.get_c_delta(self.dividend, self.expt, self.d1)
            
            self.theta = self.get_c_theta(self.current_price, self.iv,
                                          self.dividend, self.d1, self.expt,
                                          self.rate, self.strike, self.d2,
                                          self.trading_days)
            
        elif self.option_type == 'put':
            self.t_value = self.get_p_value(self.current_price,self.dividend,self.expt,self.d1,self.strike,self.rate,self.d2)
            self.delta = self.get_p_delta(self.dividend,self.expt,self.d1)
            self.theta = self.get_p_theta(self.current_price,self.iv,self.dividend,self.d1,self.expt,self.rate,self.strike,self.d2,self.trading_days)
        
        self.vega = self.get_vega(self.current_price, self.dividend,self.expt,self.d1)
        self.gamma = self.get_gamma(self.dividend,self.d1,self.current_price,self.iv,self.expt)
        
    
    def __init__(self, name, underlying_price, option_type, option_position, strike, 
                 implied_volatility, days_to_expiration, trading_days, 
                 price_paid, number_of_contracts, interest_rate = rate, 
                 commission = commission, fixed_commission = fixed_commission):
        '''
        tckr                  : Option Ticker (string)
        option_type           : put, call (string)
        option_position       : long, short (string)
        strike                : strike price of the option
        implied_volatility    : forward looking volatility of the underlying based on current option value (Decimal)
        days_to_expiration    : number of days to the expiration date
        trading_days          : number of trading days being considered in a year (252)
        price_paid            : the market price of the option (1 share)
        number_of_contracts   : the number of contracts purchased
        interest_rate         : the risk free interest rate
        '''
       
        # Fixed Variables
        self.security = 'Option'
        self.option_type = option_type
        if option_position == 'short':
            self.position = -1
        else:
            self.position = 1
            
        self.contracts = number_of_contracts * self.position
        self.strike = strike
        self.rate = interest_rate
        self.dividend = 0
        self.trading_days = trading_days
        self.price_paid = price_paid*self.contracts + commission*abs(self.contracts) + fixed_commission
        
        
        
        # Dependent Variables
        self.current_price = underlying_price
        self.expt = days_to_expiration/trading_days
        self.iv = implied_volatility
        self.hv = None
    
        if self.position == 1:
            self.tckr = name +'C '+ str(datetime.now() - timedelta(days_to_expiration))[0:10] + ' ' + str(strike)[0:5]
        else:
            self.tckr = name +'P '+ str(datetime.now() - timedelta(days_to_expiration))[0:10] + str(strike)[0:5]
        # Greek Variables and Value
        self.update_greeks()
        
    # Functions
    def get_t_value(self,price, timeshift = 0):        
        # The value of the option at some specified price
        d1 = self.get_d1(price, self.strike, self.rate, self.dividend, self.iv, self.expt - timeshift)
        d2 = self.get_d2(d1,self.iv,self.expt - timeshift)
        if self.option_type == 'call':
            return self.get_c_value(price, self.dividend,self.expt - timeshift,d1,self.strike, self.rate, d2)
        elif self.option_type == 'put':
            return self.get_p_value(price, self.dividend,self.expt - timeshift, d1, self.strike, self.rate, d2)
    
    def get_t_delta(self, price, timeshift = 0):
        
        # Delta of the option at some price
        d1 = self.get_d1(price, self.strike, self.rate, self.dividend, self.iv, self.expt - timeshift)
        if self.option_type == 'call':
            return self.get_c_delta(self.dividend, self.expt - timeshift, d1)
        elif self.option_type == 'put':
            return self.get_p_delta(self.dividend, self.expt - timeshift, d1)    
            
    def get_t_gamma(self, price, timeshift = 0):
        # gamma of the option at some price
        d1 = self.get_d1(price,self.strike,self.rate,self.dividend,self.iv,self.expt - timeshift)
        return self.get_gamma(self.dividend,d1,self.strike,self.iv,self.expt - timeshift)
        