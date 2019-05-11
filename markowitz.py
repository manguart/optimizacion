"""
This script optimize portfolio returns using Markowitz curve
"""
import numpy as np
import matplotlib.pyplot as plt
import cvxopt
from cvxopt import blas, solvers
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_pdf import PdfPages

return_data = pd.read_csv('monthly_return.csv')
return_data = return_data[[i for i in return_data.keys() if i not in ('date')]]
return_data = return_data.T.values
n_portfolios = 50000
mean_returns = np.mean(return_data, axis=1)
sigma_returns = np.cov(return_data)
number_of_optimal_values = 200


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


def optimization(N):
    """
    Find optimal solutions using cvxopt package
    """
    total_stocks = len(return_data)
    mus = [10 ** (5.0 * t / N - 1.0) for t in range(N)]
    # Covariance matrix
    Sigma = cvxopt.matrix(sigma_returns)
    # Mean matrix
    mean_return_cvx = cvxopt.matrix(mean_returns)
    # Identity matrix
    G = -cvxopt.matrix(np.eye(total_stocks))
    # Vector of zeros
    h = cvxopt.matrix(0.0, (total_stocks, 1))
    # Vector of ones
    A = cvxopt.matrix(1.0, (1, total_stocks))
    # Just 1x1 matrix
    b = cvxopt.matrix(1.0)

    portfolios = [solvers.qp(mu * Sigma, -mean_return_cvx,
                             # Constraints
                             G, h, A, b)['x'] for mu in mus]
    # Multiply weights per expected return
    expected_returns = [blas.dot(mean_return_cvx, p) for p in portfolios]
    # Ger variance
    portfolio_risk = [np.sqrt(blas.dot(p, Sigma * p)) for p in portfolios]
    m1 = np.polyfit(expected_returns, portfolio_risk, 2)
    x1 = np.sqrt(m1[2] / m1[0])
    wt = np.asarray(solvers.qp(cvxopt.matrix(x1 * Sigma), -mean_return_cvx, G, h, A, b)['x'])
    return wt, expected_returns, portfolio_risk

def main():
    """
    General calls
    """
    # Get random portfolio
    random_return, random_risk = np.column_stack([generate_portfolio() for i in range(n_portfolios)])
    random_risk = [j[0] for j in random_risk]
    random_return = [k[0] for k in random_return]

    # Optimal portfolio
    wt, optimal_returns, optimal_risks = optimization(number_of_optimal_values)

    # Plot results
    pdf = PdfPages('markowitz_curve.pdf')
    plt.figure()
    plt.plot(random_risk, random_return, 'o', markersize=5, alpha=0.5)
    plt.plot(optimal_risks, optimal_returns, 'o', alpha=0.7, color='red')
    plt.xlabel('Risk')
    plt.grid()
    plt.ylabel('Return')
    plt.title('Markowitz curve')
    pdf.savefig()
    plt.close()
    pdf.close()

if __name__ == "__main__":
    main()
