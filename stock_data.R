# This download stock data from yahoo, genrate some plots and create a csv
library(quantmod)
library(corrplot)
stockData <- new.env()
# The user can set this dates
start_date = as.Date("2009-01-01")
end_date= as.Date("2019-03-31")
# Also, user can set stocks
tickets <- c("AAPL", "AMZN", "MSFT", "GOOGL", "KO", "PEP", "JPM", "BAC", "NSANYN")
portafolio_daily_prices <- NULL
portafolio_monthly_return <- NULL
for (Ticker in tickets){
   # Get prices
   prices <- getSymbols.yahoo(Ticker, 
                              from=start_date, to = end_date, 
                              periodicity = "daily", auto.assign=FALSE)[,4]
   portafolio_daily_prices <- cbind(portafolio_daily_prices, prices)
   # Generate plots
   png(paste(Ticker, ".png", sep = ""))
   chartSeries(prices, name = Ticker)
   dev.off()
   # Monthly return
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
write.csv(x = portafolio_monthly_return, file = "monthly_return.csv")
write.csv(portafolio_monthly_return, file = "daily_price.csv")

png("correlation_returns.png")
corrplot(cor(portafolio_monthly_return))
dev.off()

