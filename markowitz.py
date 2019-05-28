# -*- coding: utf-8 -*-
##############################################################
######### se importan las librerias que seran usadas #########
import numpy as np
import pandas as pd
from cvxopt import blas, solvers, matrix


def markowitz(r_i, sigma, rho, Ventas_en_corto=False):
    ##########################################################
    # Se defienen las matrices principales con la equivalencia
    # entre el problema general de optimización y el problema
    # de optimización de markowitz
    ##########################################################
    d = len(sigma)
    P = matrix(sigma)
    q = matrix(np.zeros(d, float))
    A = matrix([
        np.ones(d, float).tolist(), r_i.tolist()
    ]).trans()
    b = matrix([1.0, float(rho)])
    ##########################################################
    # Se define la restricción para cuando las ventas en corto
    # están permitidas
    ##########################################################
    diagonal = np.zeros((d, d), float)
    np.fill_diagonal(diagonal, -1.0)

    G = matrix(diagonal)
    h = matrix(np.zeros(d, float))
    ##########################################################
    # Se revisa la condición de Ventas en corto para asignar
    # valores a G y h
    ##########################################################
    if Ventas_en_corto == True:
        G = None
        h = None
    else:
        G = G
        h = h
    ##########################################################
    # Una vez que están definidos todos los elementos se
    # resuelve el problema usando solvers.qp
    ##########################################################
    sol = solvers.qp(P=P, q=q, G=G, h=h, A=A, b=b)
    w = list(sol['x'])
    ##########################################################
    return w


###############################################################################
################################### Ejemplo ###################################
###############################################################################

# Cargamos nuestros datos
return_data = pd.read_csv('monthly_return.csv')
return_data = return_data[[i for i in return_data.keys() if i not in ('date')]]
return_data = return_data.T.values

# Obtenemos los arreglos que seran usados como inputs
mean_returns = np.mean(return_data, axis=1)
sigma_returns = np.cov(return_data)

# Cálculamos los pesos para un rendimiento dado de .009 permitiendo ventas en corto
markowitz(mean_returns, sigma_returns, .01, Ventas_en_corto=False)

# Cálculamos los pesos para un rendimiento dado de .009 solo con pesos positivos
markowitz(mean_returns, sigma_returns, .009, Ventas_en_corto=True)


