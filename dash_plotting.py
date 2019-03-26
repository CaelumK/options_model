# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 18:15:01 2018

@author: Caelum Kamps
"""

from matplotlib import pyplot as plt
import numpy as np
from io import BytesIO
import base64

def fig_to_uri(in_fig, close_all=True, **save_args):
    # type: (plt.Figure) -> str
    """
    Save a figure as a URI
    :param in_fig:
    :return:
    """
    out_img = BytesIO()
    in_fig.savefig(out_img, format='png', **save_args)
    if close_all:
        in_fig.clf()
        plt.close('all')
    out_img.seek(0)  # rewind file
    encoded = base64.b64encode(out_img.read()).decode("ascii").replace("\n", "")
    return "data:image/png;base64,{}".format(encoded)

   
def plot_time_independent(book, attributes = ['value'], step = 1):
    '''
    attributes = value, delta, gamma
    '''
    
    cp = book[0].current_price
    prices = [max(cp + i*step,0.1) for i in range(-50,50)]
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
    fig, ax1 = plt.subplots(1,1)
    
    ax1.grid()
    ax1.set_xlabel('Underlying Price ($)')
    
    if attribute == 'gamma':
        ax1.set_title('Theoretical Gamma - Time Independent')
        ax1.set_ylabel('Gamma')
    elif attribute == 'delta':
        ax1.set_title('Theoretical Delta - Time Independent')
        ax1.set_ylabel('Delta')
    else:
        ax1.set_title('Theoretical Market Value - Time Independent')
        ax1.set_ylabel('Option Price ($)')
        # Cacluating the breakeven point using the amount paid for the contracts
        paid = sum([leg.price_paid for leg in book])
        ax1.axhline(paid, color = 'y', linestyle = 'dashdot', label = 'breakeven')
        
        current_worth = -paid
        for leg in book:
            current_worth += leg.t_value*leg.contracts
    
        print('Current worth = $',str(current_worth*100)[0:5])
    
    for leg in book:
        ax1.axvline(x=leg.strike, color = 'r', linestyle = 'dashdot', label = 'Strike')
    ax1.axvline(x=leg.current_price, color = 'g', linestyle ='dashdot', label = 'Current')
    
    i = 0 
    for value in values:
        ax1.plot(prices,value, label = attributes[i])
        i+=1
        
    ax1.legend()
    out_url = fig_to_uri(fig)
    return(out_url)
    

    
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
    
    
    
    
    
    
    
    
    