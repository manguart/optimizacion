##############################################################################
# Esta función sirve para bajar los precios diarios y los retornos mensuales
# de un conjunto de acciones dadas. Recibe como input un conjunto de acciones
# fechas inicial y fecha final, el output de la función es una lista que 
# contiene un data frame con los precios diarios y otro data frame con los 
# rendimientos mensuales

##############################################################################
# cargamos las librerias que seran usadas
library(quantmod)
library(purrr)
library(readr)
library(dplyr)
library(tibble)
##############################################################################
# Definimos la función

obtener_rendimientos<-function(Activos, Fecha_inicial, Fecha_final){
  
  # bajamos los activos
  portafolio_prices<-Activos %>% 
    map(~getSymbols.yahoo(.,
                          from=Fecha_inicial, 
                          to = Fecha_final,
                          periodicity = "daily", 
                          auto.assign=FALSE)[,4])
  
  # Obtenemos los precios diarios a partir de portafolio_prices
  precios_diarios<-portafolio_prices %>% 
    map(~as.data.frame(.) %>%
          rownames_to_column(var = "date")) %>% 
    reduce(left_join, by = "date") %>% 
    set_names(c("date", Activos)) %>% 
    mutate(date = date %>% as.Date)
  
  # Obtenemos los rendimientos mensuales a partir de portafolio_prices
  rendimientos_mensuales<-portafolio_prices %>% 
    map(~monthlyReturn(.) %>% 
          as.data.frame %>% 
          rownames_to_column(var = "date")) %>% 
    reduce(left_join, by = "date") %>% 
    set_names(c("date", Activos)) %>% 
    mutate(date = date %>% as.Date)
  
  precios_y_rendimientos<-list(PreciosDiarios = precios_diarios, 
                               RendimientosMensuales = rendimientos_mensuales)
  
  return(precios_y_rendimientos)
}

##############################################################################
################################### Ejemplo ##################################
##############################################################################

# Seleccionamos algunas acciones
activos<-c("AAPL", "AMZN", "MSFT", "KO", "PEP", "JPM", 
           "BAC", "NKE", "ORCL", "IBM", "PG", "WMT")

# Obtenemos los rendimientos
preciosd_y_retornos_mensuales<-activos %>% 
  obtener_rendimientos(Fecha_inicial = as.Date("2002-01-01"),
                       Fecha_final = as.Date("2019-03-31"))

portafolio_daily_prices<-preciosd_y_retornos_mensuales$PreciosDiarios
portafolio_monthly_return<-preciosd_y_retornos_mensuales$RendimientosMensuales
##############################################################################

write_csv(portafolio_daily_prices, "daily_price.csv")
write_csv(portafolio_monthly_return, "monthly_return.csv")
