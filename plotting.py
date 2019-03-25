# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 18:15:01 2018

@author: Caelum Kamps
"""

from matplotlib import pyplot as plt

def plot_time_independent(book, attributes = ['value'], step = 1):
    '''
    attributes = value, delta, gamma
    '''
    
    cp = book[0].current_price
    prices = [cp + i*step for i in range(-50,50)]
    values = [[] for i in range(len(attributes))]
    
    i=0
    
    # Specifying prices to evalute at
    for attribute in attributes:
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
            values[i].append(v)
        i+=1

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
    
    i = 0 
    for value in values:
        plt.plot(prices,value, label = attributes[i])
        i+=1
        
    plt.legend()
    plt.show()
    

    
def plot_bleed(book, attribute = 'value', step = 1, number_of_intervals = 3, trading_days = 252):
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

def plot_hedge(book, step = 1, fdo = 0, trading_days = 365, plot_components = 0):
    # fdo := forward date offset
    
    try:
        cp = book[0].current_price
    except:
        cp = book[0].price
    prices = [cp + i*step for i in range(-50,50)]
    
    
    values = []
    
    for price in prices:
        v = 0
        for leg in book:
            if leg.security == 'Stock':
                v += leg.get_return(price)
            elif leg.security == 'Option':
                v += (leg.get_t_value(price, timeshift = fdo) - leg.price_paid)*leg.contracts*100
            else:
                None
        values.append(v)
    
    if plot_components == 1:
        component_values = []
        
        
        for leg in book:
            temp = []
            
            for price in prices:
                v = 0
                if leg.security == 'Stock':
                    v += leg.get_return(price)
                elif leg.security == 'Option':
                    v += (leg.get_t_value(price, timeshift = fdo) - leg.price_paid)*leg.contracts*100
                temp.append(v)
           
            component_values.append(temp)
            
            plt.plot(prices, component_values[-1], label = leg.security)
            
            
    plt.grid()
    plt.xlabel('Underlying Price($)')
    plt.ylabel('Book Value ($)')
    plt.title('Book Value Stress Test') 
    plt.plot(prices,values, label='Book')
    plt.legend(loc = 2)
    plt.savefig('Book Value Stress Test.png', dpi = 276)
    plt.show()
    
    
    
    
    
    
    
    
    