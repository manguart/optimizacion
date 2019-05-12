"""
This script optimize portfolio returns using Markowitz curve
"""
import numpy as np
import matplotlib.pyplot as plt
from cvxopt import blas, solvers, matrix
import pandas as pd
import matplotlib
import random
matplotlib.use('Agg')
from matplotlib.backends.backend_pdf import PdfPages

return_data = pd.read_csv('monthly_return.csv')
return_data = return_data[[i for i in return_data.keys() if i not in ('date')]]
return_data = return_data.T.values
n_portfolios = 1000000
mean_returns = np.mean(return_data, axis=1)
sigma_returns = np.cov(return_data)
number_of_optimal_values = 5


def generate_portfolio():
    """
    For a given matrix with returns, generate random portfolio
    """
    weights = np.random.random(len(return_data))
    weights /= np.sum(weights)

    x = np.asmatrix(mean_returns)
    weights_matrix = np.asmatrix(weights)
    covariance_matrix = np.asmatrix(sigma_returns)

    expected_return = weights_matrix * x.T
    risk = np.sqrt(weights_matrix * covariance_matrix * weights_matrix.T)
    return expected_return, risk

def iif(cond, iftrue=1.0, iffalse=0.0):
    return iftrue if cond else iffalse


def markowitz(mu, sigma, mu_p):
    d = len(sigma)
    P = matrix(sigma)
    q = matrix([0.0 for i in range(d)])

    G = matrix([
        [(-1.0) ** (1 + j % 2) * iif(i == j / 2) for i in range(d)]
        for j in range(2 * d)
    ]).trans()
    h = matrix([iif(j % 2) for j in range(2 * d)])

    A = matrix([
        [1.0 for i in range(d)],
        list(mu)
    ]).trans()
    b = matrix([1.0, float(mu_p)])

    sol = solvers.qp(P, q, G, h, A, b)

    w = list(sol['x'])
    return w


def main():
    """
    General calls
    """
    # Get random portfolio
    random_return, random_risk = np.column_stack([generate_portfolio() for i in range(n_portfolios)])
    random_risk = [j[0] for j in random_risk]
    random_return = [k[0] for k in random_return]

    returns_random_low = random.sample(random_return,k=20000)
    optimals = []
    [optimals.append(markowitz(mean_returns, sigma_returns, i)) for i in returns_random_low]

    optimal_means = []
    for i in optimals:
        optimal_means.append(np.dot(i, mean_returns))

    optimal_variance = []
    for i in optimals:
        variance_i = np.asmatrix(i)
        optimal_variance.append(np.sqrt(float(variance_i * sigma_returns * variance_i.T)))

    # Plot results
    pdf = PdfPages('markowitz_curve.pdf')
    plt.figure()
    plt.plot(random_risk, random_return, 'o', markersize=5, alpha=0.5)
    plt.plot(optimal_variance, optimal_means, 'o', alpha=0.7, color='red')
    plt.xlabel('Risk')
    plt.grid()
    plt.ylabel('Return')
    plt.title('Markowitz curve')
    pdf.savefig()
    plt.close()
    pdf.close()

if __name__ == "__main__":
    main()

