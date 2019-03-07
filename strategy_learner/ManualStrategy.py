import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

from util import get_data, plot_data
from marketsimcode import compute_portvals
from indicators import get_Price_SMA_Ratio, get_RSI, get_MFI

def get_portfolio_stats(port_val, daily_rf=0, sf=252):

    daily_ret = (port_val / port_val.shift(1)) - 1
    cr = (port_val[-1] / port_val[0]) - 1
    adr = daily_ret.mean()
    sddr = daily_ret.std()
    k = np.sqrt(sf)
    sr = k * np.mean(adr - daily_rf) /sddr
    return cr, adr, sddr, sr


class MannualStrategy(object):

    def __init__(self, symbol="JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv=100000):
        self.symbol = symbol
        self.sd = sd
        self.ed = ed
        self.sv = sv

    def testPolicy(self,symbol,sd,ed,sv):
        symbols = []
        symbols.append(symbol)
        dates = pd.date_range(sd, ed)
        price = get_data(symbols, dates)
        orders = []
        holdings = {sym: 0 for sym in symbols}
        lookback = 14
        psr = get_Price_SMA_Ratio(symbols,dates,lookback=14)
        rsi = get_RSI(symbols,dates,lookback=14)
        mfi = get_MFI(symbols,dates)
        
        for day in range(price.shape[0]):
            for sym in symbols:
                if (psr.ix[day, sym] < 1.05) and (rsi.ix[day, sym] < 15) and (mfi.ix[day, sym] < 10):
                    if holdings[sym] < 1000:
                        holdings[sym] = holdings[sym] + 1000
                        orders.append([price.index[day].date(), sym, 'BUY', 1000])
                    else:
                        orders.append([price.index[day].date(), sym, 'NOTHING', 0])
                elif (psr.ix[day, sym] > 0.95) and (rsi.ix[day, sym] > 55) and (mfi.ix[day, sym] > 40):
                    if holdings[sym] > -1000:
                        holdings[sym] = holdings[sym] - 1000
                        orders.append([price.index[day].date(), sym, 'SELL', 1000])
                    else:
                        orders.append([price.index[day].date(), sym, 'NOTHING', 0])
                elif (psr.ix[day, sym] < 1) and (psr.ix[day-1,sym] > 1) and (holdings[sym] < 0):
                    holdings[sym] = holdings[sym] + 1000
                    orders.append([price.index[day].date(), sym, 'BUY', 1000])
                elif (psr.ix[day, sym] > 1) and (psr.ix[day-1,sym] < 1) and (holdings[sym] > 0):
                    holdings[sym] = holdings[sym] - 1000
                    orders.append([price.index[day].date(), sym, 'SELL', 1000])
                else:
                    orders.append([price.index[day].date(), sym, 'NOTHING', 0])

        df_trades = pd.DataFrame(orders, columns=["Date", "Symbol", "Order", "Shares"])
        df_trades.set_index('Date', inplace=True)
        return df_trades

    def manual_portfolio(self, symbol, sd, ed, sv, commission=9.95, impact=0.005):
        dates = pd.date_range(sd, ed)
        symbols = []
        symbols.append(symbol)
        ms_trades = self.testPolicy(symbol, sd, ed, sv)
        portval_ms = compute_portvals(ms_trades, start_val=sv, commission=commission, impact=impact)
        normed_portval_ms = portval_ms / portval_ms.ix[0]
        cr_ms, adr_ms, sdr_ms, sr_ms = get_portfolio_stats(normed_portval_ms)
        print "Cumulative Return of {}: {}".format("Manual Strategy", cr_ms)
        print "Standard Deviation of Daily Return of {}: {}".format("Manual Strategy", sdr_ms)
        print "Mean Daily Return of {}: {}".format("Manual Strategy", adr_ms)
        return normed_portval_ms

    def benchmark_portfolio(self,symbol,sd,ed,sv,commission=9.95, impact=0.005):
        dates = pd.date_range(sd, ed)
        symbols = []
        symbols.append(symbol)
        benchmark_prices = get_data(symbols, dates)
        orders = []
        for i in range(len(benchmark_prices)):
            if i == 0:
                orders.append([benchmark_prices.index[0].date(), symbol, "BUY", 1000])
            else:
                orders.append([benchmark_prices.index[i].date(), symbol, "NOTHING", 0])
        benchmark_trades = pd.DataFrame(orders, columns=["Date", "Symbol", "Order", "Shares"])
        benchmark_trades.set_index('Date', inplace=True)
        portval_benchmark = compute_portvals(benchmark_trades,start_val=sv,commission=commission,impact=impact)
        normed_portval_benchmark = portval_benchmark/ portval_benchmark.ix[0]
        cr_benchmark, adr_benchmark, sdr_benchmark, sr_benchmark = get_portfolio_stats(portval_benchmark)
        print "Cumulative Return of {}: {}".format("Benchmark", cr_benchmark)
        print "Standard Deviation of Daily Return of {}: {}".format("Benchmark", sdr_benchmark)
        print "Mean Daily Return of {}: {}".format("Benchmark", adr_benchmark)
        return normed_portval_benchmark

if __name__ == "__main__":
    ms = MannualStrategy(symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31), sv=100000)
    df_trades = ms.testPolicy(symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31), sv=100000)
    portval_ms = ms.manual_portfolio(symbol = "JPM", sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31), sv = 100000, commission = 9.95, impact = 0.005)
    portval_benchmark = ms.benchmark_portfolio(symbol="JPM", sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31), sv = 100000,  commission = 9.95, impact=0.005)
    ax = portval_ms.plot(title="Benchmark vs. Manual Strategy", color="black", label="Manual")
    portval_benchmark.plot(ax=ax, color="blue", label="Benchmark")
    ax.set_ylabel('Normalized Value')
    ax.set_xlabel('Dates')
    long_entries = []
    short_entries = []
    

    for i in range(0,len(df_trades)):
        if df_trades.ix[i,"Order"] == "SELL":
            short_entries.append(df_trades.index[i])
        elif df_trades.ix[i,"Order"] == "BUY":
            long_entries.append(df_trades.index[i])
    for i in short_entries:
        ax.axvline(x=i, color="r")
    for i in long_entries:
        ax.axvline(x=i, color="g")

    plt.grid(True)
    plt.legend(loc=0)
    plt.savefig("Benchmark vs. Manual Strategy.png")
    plt.show()






