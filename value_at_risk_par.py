from scipy.stats import norm
import pandas_datareader.data as wb
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf

# yfinance function override
''' Function that its used to override the functionality of pandas-datareader and allow the yfinance library 
 to be used instead to access Yahoo Finance data. '''
yf.pdr_override()

ticker = ['TSLA', 'AAPL', 'MSFT', 'GOOG']
weights = np.array([0.5, 0.2, 0.2, 0.1])
startdate = '2020-01-01'
enddate = '2023-01-01'

def market_data(ticker, start_date, end_date):
   return wb.get_data_yahoo(ticker, start=start_date, end=end_date)

total_data = market_data(ticker, startdate, enddate)

returns = total_data.pct_change()
cov_matrix = returns.cov()
returns_mean = returns.mean()
portfolio_mean = returns_mean.dot(weights)
portfolio_stdev = np.sqrt(weights.T.dot(cov_matrix).dot(weights))

investment = float(20000)
mean_investment = (1+portfolio_mean)*investment
stdev_investment = investment * portfolio_stdev

conf_level = 0.05
cut = norm.ppf(conf_level, mean_investment, stdev_investment)
var_id = investment - cut
num_days = int(100)

var_array = []

print(f'With an investment of ${str(investment)}, the maximum loss of yout portofolio with {str(conf_level)}% confindece level for the next {num_days} will be:')

for i in range(1, num_days):
   var_array.append(np.round(var_id*np.sqrt(i), 2))
   print(f'To {str(i)} days VaR({str((1-conf_level)*100)}%) = {str((np.round(var_id*np.sqrt(i), 2)))}')

plt.xlabel('Days')
plt.ylabel('Maximum loss of our portfolio')
plt.title(f'Maximum loss of a portfolio in {str(num_days)} days')
plt.plot(var_array, 'b')
plt.show()
