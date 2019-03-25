# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 13:26:57 2018

@author: Caelum.kamps
"""

import security_objects as so
import plotting as p
 
# Equity Object - Used as the underlying for options
td = so.equity('TD', 76.0, 0.0391, 0, 65.0, 10)     
   
# Speficy option objects
tdc = so.option(td, 'call', 'long', 76, 0.13, 20, 365, 0.5, 1)
tdp = so.option(td, 'call', 'short', 80, 0.13, 20, 365, 0.35, 2)

# Create a portfolio of options held
book = [tdc, tdp]

#p.plot_value(book, 0.2)
#p.plot_delta(book, 0.2)
p.plot_time_independent(book, 'value', 0.5)
p.plot_time_independent(book, 'delta', 0.5)
p.plot_bleed(book , 'delta', step = 0.5)


''' 
Bleed : The effect on the option price and its greek with the passage of time
    
    forward bleed: effect of moving the portfolio forward in time
    
    backward bleed: and increase in volatility exerts the force of 
    reverse time decay
    
DdeltaDvol : the effect on delta of changing volatility
    
    Stability Test 1:
        raise the volatility and examine the delta. An increase in deltas means 
        that the positions become increasingly longer vegas in a rally and 
        shorter in a selloff. This is positive DdeltaDvol. It means that the 
        book is net short options below the money and net long options 
        above the money.
        
        this test needs to be run routinely on books in emerging market currencies
        and other products where is it not advisable to she short volatility
        when the market decreases
        
    Stability Test 2: Asymptotic Vega Test
        Check the DdeltaDvol over a series of price intervals to check how the 
        book changes with price
        
Moments (Odd moments are indicators of symmetry while even moments are indicators of convexity)
    First Moment : The delta
    
    Second Moment : The Gamma
        
    Third Moment : The Skew
        The gamma exposure in function of the asset price and becomes the 
        level of asymmetry between them. if the gamma becomes more positive 
        in a rally and more negative in the sell-off, the skew is positive
        
    Fourth Moment : The Tail 
        When the fourth moment is positive, the position is convex and 
        therefore will not absolutely murk you in a big selloff or rally

Asymptotic Delta:
    The extremes of the delta in either direction used as a quick measure of risk for a book
    
'''