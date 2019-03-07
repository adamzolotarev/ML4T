"""
    Template for implementing QLearner  (c) 2015 Tucker Balch
    
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
    
    Student Name: Sihao Wang (replace with your name)
    GT User ID: swang632 (replace with your User ID)
    GT ID: 903270437 (replace with your GT ID)
    """
import datetime as dt
import pandas as pd
import util as ut
import numpy as np
import QLearner as ql
from marketsimcode import compute_portvals
from indicators import get_RSI, get_MFI, get_Price_SMA_Ratio

def get_portfolio_stats(port_val, daily_rf=0, samples_per_year=252):

    daily_ret = (port_val / port_val.shift(1)) - 1
    cr = (port_val[-1] / port_val[0]) - 1
    adr = daily_ret.mean()
    sddr = daily_ret.std()
    k = np.sqrt(samples_per_year)
    sr = k * np.mean(adr - daily_rf)/sddr
    return cr, adr, sddr, sr

class StrategyLearner(object):

    def __init__(self, verbose=False, impact=0.0):
        self.verbose = verbose
        self.impact = impact

    def author(self):
        return 'swang632'

    def Discretization(self, df, steps):
        threshold = range(0,steps)
        step_size = df.shape[0] / (steps+1)
        df = df.sort_values()

        for i in range(0, steps):
             threshold[i] = df[i*step_size]

        indicator_df = pd.DataFrame(0,columns=['discretized_value'],index=df.index)
        indicator_df['discretized_value'] = np.searchsorted(threshold,df)
        return indicator_df

    def trade_actions(self, holding, action, ret):
        rewards = 0
        if holding == -1000:
            if action <= 1:
                rewards = -ret
            else:
                holding = 1000
                rewards = 2 * ret
        elif holding == 0:
            if action == 0:
                holding = -1000
                rewards = -ret
            elif action == 2:
                holding = 1000
                rewards = ret
        else:
            if action == 0:
                holding = -1000
                rewards = -2 * ret
            else:
                rewards = ret

        return holding, rewards

    def addEvidence(self, symbol="AAPL", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv=100000):

        syms = [symbol]
        dates = pd.date_range(sd, ed)
        total_prices = ut.get_data(syms, dates)
        prices = total_prices[syms]
        psr = get_Price_SMA_Ratio(symbols=syms,dates=dates,lookback=14)
        rsi = get_RSI(symbols=syms,dates=dates,lookback=14)
        mfi = get_MFI(symbols=syms,dates=dates,lookback=14)
        spsr = psr.ix[:,symbol]
        srsi = rsi.ix[:,symbol]
        smfi = mfi.ix[:,symbol]
        dpsr=self.Discretization(spsr,steps=5)
        drsi=self.Discretization(srsi,steps=5)
        dmfi=self.Discretization(smfi,steps=5)

        prices = prices.ix[:,symbol]
        dr = prices.copy()
        dr[0] = np.nan
        dr[1:] = (prices[1:] / prices[:-1].values) - 1

        States = dpsr * 100 + drsi + dmfi
        States = States.ix[:,'discretized_value']
        self.learner = ql.QLearner(num_states=1000, num_actions=3)
        oldprofit = 0
        for iteration in range(100):
            current_holding = 0
            total_profit = 0
            rewards = 0
            for i in range(dr.shape[0] - 1):
                if (i > 0):
                    total_profit += prices[i - 1] * current_holding * dr[i]
                state = States[i]
                if i == 0:
                    action = self.learner.querysetstate(state)
                else:
                    action = self.learner.query(state, rewards)
                holding, rewards = self.trade_actions(current_holding, action, dr[i + 1])
                current_holding = holding
            total_profit += prices[-2] * current_holding * dr[-1]
            if total_profit == oldprofit:
                break
            oldprofit = total_profit

    def testPolicy(self, symbol="AAPL", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv=100000):

        dates = pd.date_range(sd, ed)
        total_prices = ut.get_data([symbol], dates)
        syms = [symbol]
        prices = total_prices[syms]
        psr = get_Price_SMA_Ratio(symbols=syms, dates=dates, lookback=14)
        rsi = get_RSI(symbols=syms, dates=dates, lookback=14)
        mfi = get_MFI(symbols=syms, dates=dates, lookback=14)
        spsr = psr.ix[:, symbol]
        srsi = rsi.ix[:, symbol]
        smfi = mfi.ix[:, symbol]
        dpsr = self.Discretization(spsr, steps=5)
        drsi = self.Discretization(srsi, steps=5)
        dmfi = self.Discretization(smfi, steps=5)
        States = dpsr * 100 + drsi + dmfi
        States = States.ix[:, 'discretized_value']
        prices = prices.ix[:, symbol]
        dr = prices.copy()
        trades = prices.copy()
        trades[:] = 0
        dr[0] = 0
        dr[1:] = (prices[1:] / prices[:-1].values) - 1
        current_holding = 0
        total_profit = 0
        for i in range(len(dr)- 1):
            if (i > 0):
                total_profit += prices[i - 1] * current_holding * dr[i]
            state = States[i]
            action = self.learner.querysetstate(state)
            holding, rewards = self.trade_actions(current_holding, action, dr[i + 1])
            trades[i] = (holding - current_holding)
            current_holding = holding
        total_profit += prices[-2] * current_holding * dr[-1]
        trades = pd.DataFrame(trades, columns=[symbol])
        return trades

    def strategy_learner_result(self, symbol="JPM", sd=dt.datetime(2008,1,1),
                   ed=dt.datetime(2009,12,31), sv=100000, commission=0.0, impact=0.0):
        dates = pd.date_range(sd, ed)
        symbols = []
        symbols.append(symbol)
        self.addEvidence(symbol="JPM", sd=sd, ed=ed, sv=sv)
        sl_trades = self.testPolicy(symbol="JPM", sd=sd, ed=ed, sv=sv)
        df_trade = pd.DataFrame(columns=["Date", "Symbol", "Order", "Shares"])
        df_trade['Date'] = sl_trades.index
        df_trade.set_index('Date', inplace=True)
        df_trade['Symbol'] = symbol
        df_trade['Order'] = ["BUY" if x > 0 else "SELL" for x in sl_trades.values]
        df_trade['Shares'] = abs(sl_trades.values)
        portval_sl = compute_portvals(df_trade, start_val=sv, commission=commission, impact=impact)
        normed_portval_sl = portval_sl / portval_sl.ix[0]
        cr_sl, adr_sl, sdr_sl, sr_sl = get_portfolio_stats(normed_portval_sl)
        print
        print "Cumulative Return of {}: {}".format("Q Learning Strategy", cr_sl)
        print "Standard Deviation of Daily Return of {}: {}".format("Q Learning Strategy", sdr_sl)
        print "Mean Daily Return of {}: {}".format("Q Learning Strategy", adr_sl)
        return normed_portval_sl, df_trade


if __name__ == "__main__":
    print "One does not simply think up a strategy"
