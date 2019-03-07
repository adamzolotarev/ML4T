"""MC1-P2: Optimize a portfolio.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		   	  			    		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		   	  			    		  		  		    	 		 		   		 		  
All Rights Reserved  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		   	  			    		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		   	  			    		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		   	  			    		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		   	  			    		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		   	  			    		  		  		    	 		 		   		 		  
or edited.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		   	  			    		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		   	  			    		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		   	  			    		  		  		    	 		 		   		 		  
GT honor code violation.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		   	  			    		  		  		    	 		 		   		 		  
GT User ID: swang632 (replace with your User ID)
GT ID: 903270437 (replace with your GT ID)
"""  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			    		  		  		    	 		 		   		 		  
from util import get_data, plot_data
import scipy.optimize as spo
  		   	  			    		  		  		    	 		 		   		 		  
# This is the function that will be tested by the autograder  		   	  			    		  		  		    	 		 		   		 		  
# The student must update this code to properly implement the functionality  		   	  			    		  		  		    	 		 		   		 		  
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):
    
    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    prices_SPY = prices_SPY / prices_SPY.ix[0,:]
    allocs = max_sr(prices, sd, ed, syms)
    cr, adr, sddr, sr, port_val = compute_portfolio_stats(prices, allocs, rfr=0.0, sf=252)
    
    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio','SPY'], axis=1)
        df_plot = df_temp.plot(grid=True, title='Daily Potfolio Value and SPY')
        df_plot.set_xlabel("Date")
        df_plot.set_ylabel("Price")
        plt.show()
        pass
    
    return allocs, cr, adr, sddr, sr

def compute_portfolio_stats(prices, allocs, rfr = 0.0, sf = 252.0):
    normed_prices = prices / prices.ix[0,:]
    allocated = normed_prices * allocs
    port_val = allocated.sum(axis=1)
    cr = (port_val.ix[-1,:] / port_val.ix[0,:]) - 1
    daily_returns = get_daily_returns(port_val)
    adr = daily_returns.mean()
    sddr = daily_returns.std()
    adjust_returns = daily_returns - rfr
    sr = np.sqrt(sf) * (adjust_returns.mean() / sddr)
    return cr, adr, sddr, sr, port_val

def assess_portfolio_sr(allocs, prices, sd, ed, syms):
    normed_prices = prices / prices.ix[0,:]
    allocated = normed_prices * allocs
    port_val = allocated.sum(axis=1)
    daily_returns = get_daily_returns(port_val)
    sddr = daily_returns.std()
    adr = daily_returns.mean()
    sr = -adr / sddr
    return sr

def max_sr(prices, sd, ed, syms):
    n_syms = len(syms)
    allocs = np.ones((1, n_syms)) / n_syms
    allocs = np.asarray(allocs)
    bounds = [(0.0,1.0) for _ in range(n_syms)]
    cons = ({'type':'eq','fun': lambda inputs: 1.0 - np.sum(inputs)})
    options = {'disp': True}
    max = spo.minimize(assess_portfolio_sr, allocs, args=(prices, sd, ed, syms,), constraints = cons, bounds = bounds, method='SLSQP')
    return max.x

def get_daily_returns(port_val):
    daily_returns = port_val.copy()
    daily_returns[1:] = (port_val[1:] / port_val[:-1].values) - 1
    daily_returns = daily_returns[1:]
    return daily_returns

def test_code():  		   	  			    		  		  		    	 		 		   		 		  
    # This function WILL NOT be called by the auto grader  		   	  			    		  		  		    	 		 		   		 		  
    # Do not assume that any variables defined here are available to your function/code  		   	  			    		  		  		    	 		 		   		 		  
    # It is only here to help you set up and test your code  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # Define input parameters  		   	  			    		  		  		    	 		 		   		 		  
    # Note that ALL of these values will be set to different values by  		   	  			    		  		  		    	 		 		   		 		  
    # the autograder!  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    start_date = dt.datetime(2008,6,1)
    end_date = dt.datetime(2009,6,1)
    symbols = ['IBM', 'X', 'GLD', 'JPM']
  		   	  			    		  		  		    	 		 		   		 		  
    # Assess the portfolio  		   	  			    		  		  		    	 		 		   		 		  
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True)
  		   	  			    		  		  		    	 		 		   		 		  
    # Print statistics  		   	  			    		  		  		    	 		 		   		 		  
    print "Start Date:", start_date  		   	  			    		  		  		    	 		 		   		 		  
    print "End Date:", end_date  		   	  			    		  		  		    	 		 		   		 		  
    print "Symbols:", symbols  		   	  			    		  		  		    	 		 		   		 		  
    print "Allocations:", allocations  		   	  			    		  		  		    	 		 		   		 		  
    print "Sharpe Ratio:", sr  		   	  			    		  		  		    	 		 		   		 		  
    print "Volatility (stdev of daily returns):", sddr  		   	  			    		  		  		    	 		 		   		 		  
    print "Average Daily Return:", adr  		   	  			    		  		  		    	 		 		   		 		  
    print "Cumulative Return:", cr  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		   	  			    		  		  		    	 		 		   		 		  
    # This code WILL NOT be called by the auto grader  		   	  			    		  		  		    	 		 		   		 		  
    # Do not assume that it will be called  		   	  			    		  		  		    	 		 		   		 		  
    test_code()  		   	  			    		  		  		    	 		 		   		 		  
