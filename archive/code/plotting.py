# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 18:15:01 2018

@author: Caelum Kamps
"""

from matplotlib import pyplot as plt

def plot_time_independent(book, attribute = 'value', step = 1):
    '''
    attributes = value, delta, gamma
    '''
    
    cp = book[0].current_price
    prices = [cp + i*step for i in range(-50,50)]
    values = []
    
    # Specifying prices to evalute at
    values = []
    
    # Specifying prices to evalute at
    for price in prices:
        v = 0
        if attribute == 'gamma':
            for leg in book:
                v += leg.get_t_gamma(price)*leg.contracts
        elif attribute == 'delta':
            for leg in book:
                v += leg.get_t_delta(price)*leg.contracts
        else:
            for leg in book:
                v += leg.get_t_value(price)*leg.contracts
        values.append(v)
        
    
    plt.grid()
    plt.xlabel('Underlying Price ($)')
    
    if attribute == 'gamma':
        plt.title('Theoretical Gamma - Time Independent')
        plt.ylabel('Gamma')
    elif attribute == 'delta':
        plt.title('Theoretical Delta - Time Independent')
        plt.ylabel('Delta')
    else:
        plt.title('Theoretical Market Value - Time Independent')
        plt.ylabel('Option Price ($)')
        # Cacluating the breakeven point using the amount paid for the contracts
        paid = sum([leg.price_paid for leg in book])
        plt.axhline(paid, color = 'y', linestyle = 'dashdot', label = 'breakeven')
        
        current_worth = -paid
        for leg in book:
            current_worth += leg.t_value*leg.contracts
    
        print('Current worth = $',str(current_worth*100)[0:5])
    
    for leg in book:
        plt.axvline(x=leg.strike, color = 'r', linestyle = 'dashdot', label = 'Strike')
    plt.axvline(x=leg.current_price, color = 'g', linestyle ='dashdot', label = 'Current')
   
    plt.plot(prices,values)
    plt.legend()
    plt.show()
    

    
def plot_bleed(book, attribute = 'value', step = 1, number_of_intervals = 3, trading_days = 365):
    '''
    attributes = value, delta, gamma
    '''
    
    
    interval = min([leg.expt for leg in book])/number_of_intervals
    interval_days = int(interval*trading_days)

    periods = [interval*(i) for i in range(number_of_intervals)]
    
    cp = book[0].current_price
    prices = [cp + i*step for i in range(-50,50)]
    lines = []
    
    
    
    for interval in periods:
        values = []
        # Specifying prices to evalute at
        for price in prices:
            v = 0
            if attribute == 'gamma':
                for leg in book:
                    v += leg.get_t_gamma(price, timeshift = interval)*leg.contracts
            elif attribute == 'delta':
                for leg in book:
                    v += leg.get_t_delta(price, timeshift = interval)*leg.contracts
            else:
                for leg in book:
                    v += leg.get_t_value(price, timeshift = interval)*leg.contracts
            values.append(v)
        lines.append(values)
    
    plt.grid()
    plt.xlabel('Underlying Price ($)')
    
    if attribute == 'gamma':
        plt.title('Gamma Bleed')
        plt.ylabel('Gamma')
    elif attribute == 'delta':
        plt.title('Delta Bleed')
        plt.ylabel('Delta')
    else:
        plt.title('Option Price Bleed')
        plt.ylabel('Value ($)')
        
        # Cacluating the breakeven point using the amount paid for the contracts
        paid = sum([leg.price_paid for leg in book])
        plt.axhline(paid, color = 'y', linestyle = 'dashdot', label = 'breakeven')
        
    for leg in book:
        plt.axvline(x=leg.strike, color = 'r', linestyle = 'dashdot', label = 'Strike')
    
    plt.axvline(x=leg.current_price, color = 'g', linestyle ='dashdot', label = 'Current')
    

    for i in range(len(lines)):
        plt.plot(prices,lines[i], label = 't + ' + str(int(interval_days*i)) + ' days')

        
    plt.legend()
    plt.show()


    
    
    
    
    
    
    