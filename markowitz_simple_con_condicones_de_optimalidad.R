############################################################################
# Está función cálcula los pesos optimos w_i con ventas en corto. 
# el output es un data.frame con los w_i's optimos y 
# coeficientes de penalización. La función recibe los siguientes inputs:
# r_i: un vactor que contiene todos los promedios de los activos
# Sigma: una matriz de varianzas y covarianzas de los activos
# rho: un rendimiento deseado
############################################################################
# Cargamos las librerias que usaremos
library(readr)
library(dplyr)

# Definimos la función
markowitz_simple_con_condicones_de_optimalidad<-function(r_i, Sigma, rho){
  ##########################################################################
  # Definimos la matriz de Karush–Kuhn–Tucker
  kkt_matrix<-(2*Sigma) %>% 
    rbind(1) %>% 
    rbind(r_i) %>% 
    cbind(c(rep(1.0,ncol(Sigma)),0.0, 0.0)) %>% 
    cbind(c(r_i, 0, 0))
  ##########################################################################
  # Definimos la parte derecha del sistema de ecuaciones a resolver
  b<-c(rep(0,ncol(Sigma)),1, rho)
  ##########################################################################
  # Se cáclucla la solución del problema
  w_i<-solve(kkt_matrix, b, tol = 1e-7) %>% 
    as.data.frame
  ##########################################################################
  return(w_i)
}

############################################################################
################################### Ejemplo ################################
############################################################################

# Cargamos nuestros datos
returns<- 'monthly_return.csv' %>%
  read_csv %>%
  select(-date)

# Calculamos los inputs que necesitaremos
sigma_returns<-cov(returns)
mean_returns<-colMeans(returns)

# aplicamos la función para un rendimiento dado de .009
markowitz_simple_con_condicones_de_optimalidad(mean_returns, sigma_returns, .009)

Sigma = 1
r_i = 1
rho = 1

kkt_matrix<-(2*Sigma) %>%
  rbind(1) %>%
  rbind(r_i) %>%
  cbind(c(rep(1.0,ncol(Sigma)),0.0, 0.0)) %>%
  cbind(c(r_i, 0, 0))
  # Lado derecho
  b<-c(rep(0,ncol(Sigma)),1, rho)
  # Solucion del problema
  w_i <- solve(kkt_matrix, b, tol = 1e-7) %>% as.data.frame

  w_i + 2




