library(readr)
data <- read_csv("C:/04. IT Projects/PROJECTS/0. AI Projects/NEWS_ANALYTICS/Stocks_analysis/Stocks_list/MacroTrends_Data_Download_A.csv", 
                 skip = 13)
View(data)
values <- data[,c('date', 'open')]
plot(values$date, values$open, main="test")
library(ggplot2)
ggplot(data, aes(x=date, y=open)) + geom_point(shape=1) + geom_smooth() + coord_cartesian(ylim=c(20,60)) 
x <- values['date']
y <- values['open']
y1 <- as.numeric(unlist(y))
m1 <- smooth.spline(x1, y1)
plot(x1, m1)
length(values)                                                                                          
x1 <- 1:5154
y1 <- as.vector(y)
plot.new()
ggplot(x1, y1) + geom_point(shape=1) + geom_smooth() + coord_cartesian(ylim=c(20,60))
lines(fitted(m1) ~ x1, lty = "solid", col = "darkolivegreen", lwd = 2)
