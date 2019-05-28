#########################################################################
################################## EDA ##################################
#########################################################################
# Cargamos las librerias que usaremos
library(readr)
library(ggplot2)
library(tidyr)
library(dplyr)
library(ggridges)
library(viridis)
library(lubridate)
library(ggcorrplot)
#########################################################################
# Cargamos los datos que usaremos
retornos_mensuales<-read_csv("monthly_return.csv")
precios_diarios<-read_csv("daily_price.csv")
#########################################################################
# Boxplots para rendimientos mensuales del 2014 al 2019
retornos_mensuales %>% 
  gather(Activo, rendimiento, -date) %>% 
  mutate(Year = year(date) ) %>%
  filter(Year %in% c(2014, 2015, 2016, 2017, 2018, 2019)) %>% 
  ggplot(aes(x = Activo, y = rendimiento)) +
  #scale_y_log10() +
  geom_boxplot(outlier.colour = "hotpink") +
  geom_jitter(position = position_jitter(width = 0.1, height = 0), 
              alpha = 1/4)+
  theme_bw() +
  coord_flip() 
#########################################################################
# correlaciones mensuales para todos los datos
round(cor(retornos_mensuales %>% select(-date)), 1) %>% 
  ggcorrplot(hc.order = TRUE, type = "lower",
           outline.col = "white",
           ggtheme = ggplot2::theme_gray,
           colors = c("#6D9EC1", "white", "#E46726")) +
  theme_minimal()
#########################################################################
# Series de los precios diarios
precios_diarios %>% 
  gather(Activo, rendimiento, -date) %>% 
  mutate(Year = year(date) ) %>% 
  ggplot(aes(x = date, y = rendimiento)) + 
  geom_line(aes(color = Activo), size = 1) +
  stat_smooth(
    color = "#FC4E07", fill = "#FC4E07",
    method = "loess") +
  scale_y_log10()+
  scale_color_viridis(discrete=TRUE) +
  theme_minimal() +
  theme(legend.position = "none", axis.text.x = element_text(angle = 90)) +
  facet_wrap(~Activo, ncol=3)
