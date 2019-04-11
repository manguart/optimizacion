import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_pdf import PdfPages

monthly_returns = pd.read_csv('monthly_return.csv')
monthly_returns_mean = monthly_returns.mean()
covariance_matrix = monthly_returns.cov()

num_assets = len(monthly_returns.keys()) - 1
num_portfolios = 500000

rf = 0.08 / 12

port_returns = []
port_volatility = []
stock_weights = []
for single_portfolio in range(num_portfolios):
    weights = np.random.random(num_assets)
    weights /= np.sum(weights)
    returns = np.dot(weights, monthly_returns_mean)
    volatility = np.sqrt(np.dot(weights.T, np.dot(covariance_matrix, weights)))
    port_returns.append(returns)
    port_volatility.append(volatility)
    stock_weights.append(weights)


summary_portafolio = pd.DataFrame(stock_weights, columns=monthly_returns_mean.keys())
summary_portafolio['return'] = port_returns
summary_portafolio['volatility'] = np.sqrt(port_volatility)
summary_portafolio['sharpe_ratio'] = (summary_portafolio['return'] - rf)/summary_portafolio['volatility']

max_sharpe_idx = np.argmax(summary_portafolio['sharpe_ratio'])
minimum_volatility = np.argmin(summary_portafolio['volatility'])

max_sharpe = summary_portafolio.iloc[max_sharpe_idx]
min_volatility = summary_portafolio.iloc[minimum_volatility]


pdf = PdfPages('markowitz_curve.pdf')
plt.figure()
plt.scatter(summary_portafolio['volatility'], summary_portafolio['return'], alpha=0.1)
plt.scatter(max_sharpe['volatility'],max_sharpe['return'], marker='*', color='g', s=100, label='Maximum Sharpe')
plt.scatter(min_volatility['volatility'],min_volatility['return'], marker='*', color='r', s=100, label='Minimum volatility')
plt.legend(loc='best')
plt.grid(True)
plt.title('Markowitz curve')
plt.xlabel('Volatility')
plt.ylabel('Expected Return')
pdf.savefig()
plt.close()
pdf.close()