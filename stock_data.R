library(quantmod)
library(corrplot)
stockData <- new.env()
# El usuario puede variar estas fechas
startDate = as.Date("2009-01-01")
endDate= as.Date("2019-03-31")
# El usuario puede agregar a su voluntad esto
tickets <- c("AAPL", "AMZN", "MSFT", "GOOGL", "KO", "PEP", "JPM", "BAC", "NSANYN")
portafolio_daily_prices <- NULL
portafolio_monthly_return <- NULL
for (Ticker in tickets){
   # Obtener precios
   prices <- getSymbols.yahoo(Ticker, 
                                    from=startDate, to = endDate, 
                                    periodicity = "daily", auto.assign=FALSE)[,4]
   portafolio_daily_prices <- cbind(portafolio_daily_prices, prices)
   # Generar grafico
   png(paste(Ticker, ".png", sep = ""))
   chartSeries(prices, name = Ticker)
   dev.off()
   # Rendimiento mensual
   portafolio_monthly_return <- cbind(portafolio_monthly_return, monthlyReturn(prices))
}

# Limpiar el dataset y ponerlo en un CSV
names_portafolio_prices <- names(portafolio_daily_prices)

replace_close <- function(str){
   return(gsub(pattern = ".Close", x = str, replacement = ""))
}

nombres <- sapply(names_portafolio_prices, replace_close)

names(portafolio_monthly_return) <- nombres
names(portafolio_daily_prices) <- nombres

# Escritura en csv
write.csv(x = portafolio_monthly_return, file = "rendimiento_mensual.csv")
write.csv(portafolio_monthly_return, file = "precio_mensual.csv")

png("correlation_returns.png")
corrplot(cor(portafolio_monthly_return))
dev.off()

