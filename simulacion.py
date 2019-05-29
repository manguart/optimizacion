# -*- coding: utf-8 -*-
"""
This script optimize portfolio returns using Markowitz curve
"""
import numpy as np
import matplotlib.pyplot as plt
from markowitz import markowitz
import pandas as pd
import matplotlib
import random
matplotlib.use('Agg')
from matplotlib.backends.backend_pdf import PdfPages

return_data = pd.read_csv('monthly_return.csv')
return_data = return_data[[i for i in return_data.keys() if i not in ('date')]]
return_data = return_data.T.values
n_portfolios = 500000
mean_returns = np.mean(return_data, axis=1)
sigma_returns = np.cov(return_data)


def generate_portfolio():
    """
    For a given matrix with returns, generate random portfolio
    W are the weights of stocks in a given portfolio
    sum(w) = 1
    Sigma is the covariance matrix
    Expected return form portfolio = w * x^T
    Portfolio variance = w * Sigma * w^T

    The simulation process consist in generate some random weights and get
    the variance and expected returns for those random weights. If you do this many times
    you will find the optimal values for a particular portfolio allocation balancing
    risk and reward
    """
    w = np.random.random(len(return_data))
    w /= np.sum(w)

    x = np.asmatrix(mean_returns)
    w_matrix = np.asmatrix(w)
    covariance_matrix = np.asmatrix(sigma_returns)

    expected_return = w_matrix * x.T
    risk = np.sqrt(w_matrix * covariance_matrix * w_matrix.T)
    return risk, expected_return


def main():
    """
    General calls
    """
    # Get random portfolio
    random_risk, random_return = np.column_stack([generate_portfolio() for i in range(n_portfolios)])
    random_risk = [j[0] for j in random_risk]
    random_return = [k[0] for k in random_return]

    returns_random_low = random.sample(random_return, k=20000)
    optimals = [markowitz(mean_returns, sigma_returns, i) for i in returns_random_low]
    optimal_means = [np.dot(i, mean_returns) for i in optimals]

    optimal_variance = [np.sqrt(float(np.asmatrix(i) * sigma_returns * np.asmatrix(i).T)) for i in optimals]

    # Plot results
    pdf = PdfPages('markowitz_curve.pdf')
    plt.figure()
    plt.plot(random_risk, random_return, 'o', markersize=5, alpha=0.5)
#    plt.plot(optimal_variance, optimal_means, 'o', alpha=0.7, color='red')
    plt.xlabel('Risk')
    plt.grid()
    plt.ylabel('Return')
    plt.title('Markowitz curve')
    pdf.savefig()
    plt.close()
    pdf.close()

if __name__ == "__main__":
    main()
