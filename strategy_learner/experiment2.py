import ManualStrategy as mas
import StrategyLearner as sl
import datetime as dt
import matplotlib.pyplot as plt


def experiment2():

    ms = mas.MannualStrategy(symbol="JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv=100000)
    portval_benchmark = ms.benchmark_portfolio(symbol="JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv=100000, commission=0.0, impact=0.005)
    stl = sl.StrategyLearner()
    portval_stl, trades_sbl = stl.strategy_learner_result(symbol="JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv=100000, commission=0.0, impact=0.005)
    ax = portval_stl.plot(title="Experiment 2-1. Benchmark vs Q Learning Strategy (impact=0.005)", color="black", label="Q Learning Strategy")
    short_entries = []
    long_entries = []
    
    for i in range(0, len(trades_sbl)):
        if trades_sbl.ix[i, "Order"] == "SELL":
            short_entries.append(trades_sbl.index[i])
        elif trades_sbl.ix[i, "Order"] == "BUY":
            long_entries.append(trades_sbl.index[i])
    for day in long_entries:
        ax.axvline(x=day, color="g")
    plt.grid(True)
    portval_benchmark.plot(ax=ax, color="blue", label="Benchmark")
    ax.set_ylabel('Normalized Value')
    ax.set_xlabel('Dates')
    plt.legend(loc=0)
    plt.savefig("Experiment 2-1.png")
    plt.show()
    portval_benchmark = ms.benchmark_portfolio(symbol="JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv=100000, commission=0.0, impact=0.03)
    portval_stl, trades_sbl = stl.strategy_learner_result(symbol="JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv=100000, commission=0.0, impact=0.03)
    plt.grid(True)
    ax = portval_stl.plot(title="Experiment 2-2. Benchmark vs Q Learning Strategy (impact=0.03)", color="black", label="Q Learning Strategy")
    portval_benchmark.plot(ax=ax, color="blue", label="Benchmark")
    short_entries = []
    long_entries = []

    for i in range(0, len(trades_sbl)):
        if trades_sbl.ix[i, "Order"] == "SELL":
            short_entries.append(trades_sbl.index[i])
        elif trades_sbl.ix[i, "Order"] == "BUY":
            long_entries.append(trades_sbl.index[i])
    
    for day in long_entries:
        ax.axvline(x=day, color="g")

    ax.set_ylabel('Normalized Value')
    ax.set_xlabel('Dates')
    plt.legend(loc=0)
    plt.savefig("Experiment 2-2.png")
    plt.show()

if __name__ == '__main__':
    experiment2()
