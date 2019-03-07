import ManualStrategy as mas
import StrategyLearner as sl
import datetime as dt
import matplotlib.pyplot as plt

def author():
    return'swang632'

def experiment1():

    ms = mas.MannualStrategy(symbol="JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv=100000)
    portval_ms = ms.manual_portfolio(symbol="JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv=100000, commission=0.0, impact=0.0)
    portval_benchmark = ms.benchmark_portfolio(symbol="JPM", sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv=100000, commission=0.0, impact=0.0)
    stl = sl.StrategyLearner()
    portval_stl, trades = stl.strategy_learner_result(symbol="JPM", sv=100000, sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), commission=0.0, impact=0.00)
    ax = portval_stl.plot(title="Experiment 1. Manual Strategy vs Benchmark vs Q Learning Strategy", fontsize=12, color="red", label="Q Learning Strategy")
    portval_benchmark.plot(ax=ax, color="blue", label="Benchmark")
    portval_ms.plot(ax=ax, color="black", label="Manual Strategy")
    ax.set_ylabel('Normalized Value')
    ax.set_xlabel('Dates')
    plt.grid(True)
    plt.legend(loc=0)
    plt.savefig("Experiment1.png")
    plt.show()

if __name__ == '__main__':
    experiment1()
