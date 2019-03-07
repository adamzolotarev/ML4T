import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

from util import get_data, plot_data
from marketsimcode import compute_portvals

def get_portfolio_stats(port_val, daily_rf=0, sf=252):

    daily_ret = (port_val / port_val.shift(1)) - 1
    cr = (port_val[-1] / port_val[0]) - 1
    adr = daily_ret.mean()
    sddr = daily_ret.std()
    k = np.sqrt(sf)
    sr = k * np.mean(adr - daily_rf) /sddr
    return cr, adr, sddr, sr

class theoreticallyOptimalStrategy(object):

    def __init__(self,symbol="JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31),sv=100000):
        self.symbol=symbol
        self.sd=sd
        self.ed=ed
        self.sv=sv

    def testPolicy(self,symbol,sd,ed,sv):
        symbols=[]
        symbols.append(symbol)
        dates=pd.date_range(sd,ed)
        price=get_data(symbols,dates)
        order_list = []
        curr_holding = 0

        for i in range(len(price)-1):
            if price.ix[i, symbol] == price.ix[i + 1, symbol]:
                order_list.append([price.index[i].date(),symbol,"NOTHING",0])
            elif price.ix[i, symbol] > price.ix[i + 1, symbol]:
                if curr_holding == 0:
                    curr_holding = -1000
                    order_list.append([price.index[i].date(), symbol, "SELL", 1000])
                elif curr_holding > 0:
                    curr_holding = -1000
                    order_list.append([price.index[i].date(), symbol, "SELL", 1000])
                    order_list.append([price.index[i].date(), symbol, "SELL", 1000])
                else:
                    order_list.append([price.index[i].date(), symbol, "NOTHING", 0])
            else:
                if curr_holding == 0:
                    curr_holding = 1000
                    order_list.append([price.index[i].date(), symbol, "BUY", 1000])
                elif curr_holding > 0:
                    order_list.append([price.index[i].date(), symbol, "NOTHING", 0])
                else:
                    curr_holding = 1000
                    order_list.append([price.index[i].date(), symbol, "BUY", 1000])
                    order_list.append([price.index[i].date(), symbol, "BUY", 1000])

        order_list.append([price.index[-1].date(),symbol,"NOTHING",0])
        df_trades = pd.DataFrame(order_list, columns=["Date", "Symbol", "Order", "Shares"])
        df_trades.set_index('Date',inplace=True)
        return df_trades


    def get_tos_portfolio(self,symbol,sd,ed,sv,commission=0,impact=0):
        dates = pd.date_range(sd, ed)
        symbols = []
        symbols.append(symbol)
        tos_prices = get_data(symbols,dates)
        tos_prices.sort_index()

        tos_trades = self.testPolicy(symbol,sd,ed,sv)
        portval_tos = compute_portvals(tos_trades, start_val=sv, commission=0, impact=0)
        normed_portval_tos = portval_tos/portval_tos.ix[0]
        cr_tos, adr_tos, sdr_tos, sr_tos = get_portfolio_stats(normed_portval_tos)
        print "Cumulative Return of {}: {}".format("Theoretical Optimal Strategy Out of Sample", cr_tos)
        print "Standard Deviation of daily return of {}: {}".format("Theoretical Optimal Strategy Out of Sample", sdr_tos)
        print "Mean Daily Return of {}: {}".format("Theoretical Optimal Strategy Out of Sample", adr_tos)
        return normed_portval_tos

    def get_benchmark_portfolio(self,symbol,sd,ed,sv,commission=0,impact=0):
        dates = pd.date_range(sd, ed)
        symbols = []
        symbols.append(symbol)
        benchmark_prices = get_data(symbols, dates)
        orders = []
        for i in range(len(benchmark_prices)):
            if i==0:
                orders.append([benchmark_prices.index[0].date(), symbol, "BUY", 1000])
            else:
                orders.append([benchmark_prices.index[i].date(), symbol, "NOTHING", 0])

        benchmark_trades = pd.DataFrame(orders, columns=["Date", "Symbol", "Order", "Shares"])
        benchmark_trades.set_index('Date', inplace=True)
        portval_benchmark = compute_portvals(benchmark_trades,start_val=sv,commission=commission,impact=impact)

        normed_portval_benchmark = portval_benchmark/ portval_benchmark.ix[0]
        cr_benchmark, adr_benchmark, sdr_benchmark, sr_benchmark = get_portfolio_stats(portval_benchmark)
        print "Cumulative Return of {}: {}".format("Benchmark", cr_benchmark)
        print "Standard Deviation of daily return of {}: {}".format("Benchmark", sdr_benchmark)
        print "Mean Daily Return of {}: {}".format("Benchmark", adr_benchmark)
        return normed_portval_benchmark

if __name__ == "__main__":

    tos = theoreticallyOptimalStrategy()
    df_trades = tos.testPolicy(symbol="JPM", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31),sv=100000)
    portval_tos = tos.get_tos_portfolio(symbol="JPM", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv=100000, commission=0, impact=0)
    portval_benchmark = tos.get_benchmark_portfolio(symbol="JPM", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv=100000, commission=0, impact=0)
    ax = portval_tos.plot(title="Benchmark vs. Theoretically Optimal Strategy Out of Sample", fontsize=12, color = "black",label = "Optimal Strategy")
    portval_benchmark.plot(ax = ax, color = "blue", label = "Benchmark")
    ax.set_xlabel('Dates')
    ax.set_ylabel('Normalized Value')
    plt.grid(True)
    plt.legend(loc=0)
    plt.savefig("Benchmark vs. Theoretically Optimal Strategy Out of Sample.png")
    plt.show()




