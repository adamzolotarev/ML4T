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
    
    Student Name: Sihao Wang (replace with your name)
    GT User ID: swang632 (replace with your User ID)
    GT ID: 903270437 (replace with your GT ID)
    """

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from util import get_data, plot_data

def get_Price_SMA_Ratio(symbols,dates,lookback=14):
    df = get_data(symbols,dates)
    price = df/df.values[0]
    sma = pd.rolling_mean(price,window=lookback)
    psr = price/sma
    return psr


def get_RSI(symbols, dates, lookback):
    df = get_data(symbols, dates)
    price = df / df.values[0]
    rsi = price.copy()
    for day in range(price.shape[0]):
        for sym in symbols:
            up_gain = 0
            down_loss = 0
            for prev_day in range(day-lookback+1,day+1):
                delta = price.ix[prev_day,sym]-price.ix[prev_day-1,sym]
                if delta >= 0:
                    up_gain = up_gain+delta
                else:
                    down_loss = down_loss-delta
            if down_loss == 0:
                rsi.ix[day,sym] = 100
            else:
                rs = up_gain/down_loss
                rsi.ix[day,sym] = 100-(100/(1+rs))
    return rsi


def get_MFI(symbols,dates,lookback=14):
    df = get_data(symbols, dates)
    high = get_data(symbols=symbols, dates=dates, colname="High")
    high = high/high.values[0]
    low = get_data(symbols=symbols, dates=dates, colname="Low")
    low = low/low.values[0]
    close = get_data(symbols=symbols, dates=dates, colname="Close")
    close = close/close.values[0]
    volume = get_data(symbols=symbols, dates=dates, colname="Volume")
    volume = volume/volume.values[0]
    
    typical_price = (high + low + close) / 3
    money_flow = typical_price * volume
    
    dc_tprice = typical_price.copy()
    dc_tprice.values[1:, :] = typical_price.values[1:, :] - typical_price.values[:-1, :]
    dc_tprice.values[0, :] = 0
    up_flow = money_flow[dc_tprice > 0].fillna(0).cumsum()
    down_flow = money_flow[dc_tprice < 0].fillna(0).cumsum()
    
    positive_flow = pd.DataFrame(data=0, index=df.index, columns=df.columns)
    positive_flow.values[lookback:, :] = up_flow.values[lookback:, :] - up_flow.values[:-lookback, :]
    negative_flow = pd.DataFrame(data=0, index=df.index, columns=df.columns)
    negative_flow.values[lookback:, :] = down_flow.values[lookback:, :] - down_flow.values[:-lookback, :]
    
    ms = positive_flow / negative_flow
    mfi = 100 - (100 / (1 + ms))
    mfi[mfi == np.Inf] = 100
    return mfi

def helper(symbols, dates,lookback):
    df = get_data(symbols, dates)
    price = df / df.values[0]
    original_price = df
    sma = price.copy()
    
    for day in range(price.shape[0]):
        for sym in symbols:
            sma.ix[day,sym]=0

    for day in range(price.shape[0]):
        if day < lookback:
            for sym in symbols:
                sma.ix[day,sym]=np.nan
            continue
        for sym in symbols:
            for prev_day in range (day-lookback+1, day+1):
                sma.ix[day,sym]=sma.ix[day,sym]+price.ix[prev_day,sym]
            sma.ix[day,sym]=sma.ix[day,sym]/lookback

    return price, original_price, sma

if __name__ == "__main__":

    price,original_price,sma = helper(['JPM'],dates=pd.date_range("2008-1-1","2009-12-31"),lookback=14)
    price.drop(['SPY'], axis=1, inplace=True)
    original_price.drop(['SPY'], axis=1, inplace=True)
    sma.drop(['SPY'], axis=1, inplace=True)

    psr = get_Price_SMA_Ratio(["JPM"],dates=pd.date_range("2008-1-1","2009-12-31"),lookback=14)
    psr.drop(['SPY'], axis=1, inplace=True)
    ax1 = psr.plot( title="Normalized Price_SMA_Ratio vs. Price and SMA",linewidth=1)
    price.plot(ax = ax1, linewidth = 1)
    sma.plot(ax = ax1, linewidth = 1)
    plt.grid(True)
    plt.legend(['Price/SMA Ratio','Normalized Price','SMA'])
    plt.savefig("Normalized Price_SMA_Ratio vs. Price and SMA.png")

    mfi = get_MFI(["JPM"],dates=pd.date_range("2008-1-1","2009-12-31"),lookback=14)
    mfi.drop(['SPY'], axis=1, inplace=True)
    ax2 = mfi.plot(title="MFI vs. Price", linewidth = 1)
    original_price.plot(ax = ax2,linewidth = 1)
    plt.grid(True)
    plt.legend(['MFI','Price'])
    plt.savefig("MFI vs. Price.png")
    
    rsi = get_RSI(["JPM"], dates=pd.date_range("2008-1-1", "2009-12-31"), lookback=14)
    rsi.drop(['SPY'], axis=1, inplace=True)
    ax3 = rsi.plot(title="RSI vs. Price",linewidth=1)
    original_price.plot(ax = ax3, linewidth=1)
    plt.grid(True)
    plt.legend(['RSI','Price'])
    plt.savefig("RSI vs. Price.png")
    




