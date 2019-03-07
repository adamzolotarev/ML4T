"""MC2-P1: Market simulator.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
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
GT User ID: tb34 (replace with your User ID)  		   	  			    		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		   	  			    		  		  		    	 		 		   		 		  
"""  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
import pandas as pd  		   	  			    		  		  		    	 		 		   		 		  
import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			    		  		  		    	 		 		   		 		  
import os  		   	  			    		  		  		    	 		 		   		 		  
from util import get_data, plot_data  		   	  			    		  		  		    	 		 		   		 		  


def author():
    return 'swang632'  # replace tb34 with your Georgia Tech username.

df_trades = pd.DataFrame(columns=['Date', 'Symbol', 'Order', 'Shares'])
df_trades.set_index('Date',inplace=True)

def compute_portvals(df_trades, start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code  		   	  			    		  		  		    	 		 		   		 		  
    # NOTE: orders_file may be a string, or it may be a file object. Your  		   	  			    		  		  		    	 		 		   		 		  
    # code should work correctly with either input  		   	  			    		  		  		    	 		 		   		 		  
    # TODO: Your code here  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months
    orders = pd.DataFrame(data=df_trades)
    orders = orders.sort_index()
    symbols = list(set(orders['Symbol'].values))
    orders.index = pd.to_datetime(orders.index)
    start_date = orders.index.values[0]
    end_date = orders.index.values[-1]
    dates = pd.date_range(start_date, end_date)
    prices = get_data(symbols, dates)
    prices['Cash'] = np.ones(prices.shape[0])
    stock_shares = prices * 0.0
    stock_shares.iloc[0,-1] = start_val
    order = orders.iloc[0]
    for ind, rows in orders.iterrows():
        stock_name = rows[0]
        price = prices[stock_name].ix[ind]
        unit = rows[2]
        if rows[1] == 'BUY':
            sign = -1
            stock_shares.loc[ind, stock_name] -= unit * sign
            stock_shares.loc[ind, 'Cash'] += unit * price * sign
            stock_shares.loc[ind, 'Cash'] -= unit * price * impact
            stock_shares.loc[ind, 'Cash'] -= commission
        elif rows[1] == 'SELL':
            sign = 1
            stock_shares.loc[ind, stock_name] -= unit * sign
            stock_shares.loc[ind, 'Cash'] += unit * price * sign
            stock_shares.loc[ind, 'Cash'] -= unit * price * impact
            stock_shares.loc[ind, 'Cash'] -= commission

    for i in range(1, stock_shares.shape[0]):
        for j in range(0, stock_shares.shape[1]):
            stock_shares.iloc[i,j] += stock_shares.iloc[i-1,j]

    port_vals = prices * stock_shares
    port_vals['port_val'] = port_vals.sum(axis=1)
    port_vals['daily_returns'] = (port_vals['port_val'][1:] / port_vals['port_val'][:-1].values) - 1
    port_vals['daily_returns'][0] = 0
    
    portvals = port_vals.iloc[:,-2]
    return portvals  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
		   	  			    		  		  		    	 		 		   		 		  
