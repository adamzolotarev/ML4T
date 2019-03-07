In this project, I have 7 .py files 

indicators.py
TheoreticalOptimalStrategy.py
TheoreticalOptimalStrategyOut.py
ManualStrategy.py
ComparativeAnalysis.py
marketsimcode.py
util.py


Run indicators.py to generate three charts for technical indicators

Run TheoreticalOptimalStrategy.py to create order file for theoretical optimal strategy for the in sample data(year 2008 and year 2009), get summary report of performance of theoretical optimal strategy and benchmark strategy, and make a chart to simulate the normalized portfolios of both for part 2 of the report.

Run TheoreticalOptimalStrategyOut.py to create order file for theoretical optimal strategy for the out of sample data(year 2010 and year 2011), get summary report of performance of theoretical optimal strategy and benchmark strategy, and make a chart to simulate the normalized portfolios of both for part 4 of the report.

Run ManualStrategy.py to conduct manual rule strategy, create order files for the strategy for the in sample data(year 2008 and year 2009), and generate chart to simulate normalized portfolios over in sample period in part 3 of the report. 

Run ComparativeAnalysis.py to conduct comparative analysis, create order files for the strategy for the out of sample data(year 2010 and year 2011), and generate chart to simulate normalized portfolios over out sample period in part 4 of the report. It is the exact same as ManualStrategy.py, except for the dates.

marketsimcode.py is used to simulate portfolio from trade dataframe. 

util.py is used to get price and volume data from historical price files of stocks