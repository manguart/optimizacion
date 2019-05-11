# This script download some stocks (tickets) and create som .csv and time series for exploratory purposes
library(quantmod)
library(corrplot)
# The user can set this dates
start_date = as.Date("2002-01-01")
end_date= as.Date("2019-03-31")
# Also, user can set stocks
tickets <- c("AAPL", "AMZN", "MSFT", "KO", "PEP", "JPM", "BAC", "NKE", "ORCL", "IBM", "PG", "WMT")
portafolio_daily_prices <- NULL
portafolio_monthly_return <- NULL
for (Ticker in tickets){
   # Obtener precios
   prices <- getSymbols.yahoo(Ticker,
                              from=start_date, to = end_date,
                              periodicity = "daily", auto.assign=FALSE)[,4]
   portafolio_daily_prices <- cbind(portafolio_daily_prices, prices)
   # Generar grafico
   png(paste(Ticker, ".png", sep = ""))
   chartSeries(prices, name = Ticker)
   dev.off()
   # Rendimiento mensual
   portafolio_monthly_return <- cbind(portafolio_monthly_return, monthlyReturn(prices))
}

# Clean dataset, add it to a .csv
names_portafolio_prices <- names(portafolio_daily_prices)

replace_close <- function(str){
   return(gsub(pattern = ".Close", x = str, replacement = ""))
}

names_columns <- sapply(names_portafolio_prices, replace_close)

names(portafolio_monthly_return) <- names_columns
names(portafolio_daily_prices) <- names_columns

# Write to .csv
portafolio_daily_prices <- data.frame(portafolio_daily_prices)
portafolio_monthly_return <- data.frame(portafolio_monthly_return)

portafolio_monthly_return$date <- as.Date(index(portafolio_monthly_return))
portafolio_daily_prices$date <- as.Date(index(portafolio_daily_prices))

write.csv(x = portafolio_monthly_return, file = "monthly_return.csv", row.names=FALSE)
write.csv(x = portafolio_daily_prices, file = "daily_price.csv", row.names=FALSE)
