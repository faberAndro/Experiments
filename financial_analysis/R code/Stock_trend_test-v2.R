library(readr)
data <- read_csv("C:/04. IT Projects/PROJECTS/0. AI Projects/NEWS_ANALYTICS/Stocks_analysis/Stocks_list/MacroTrends_Data_Download_A.csv", 
                 skip = 13)
View(data)
y1 <- data['open']
y <- as.numeric(unlist(y1))
xt <- 1:5154
time <- 1:5154

library(mgcv)

m1 <- smooth.spline(xt, y)
m2 <- gam(y ~ s(xt, k = 20))
# m3 <- gamm(y ~ s(xt, k = 20), correlation = corAR1(form = ~ time))

edf2 <- summary(m2)$edf
# edf3 <- summary(m3$gam)$edf

plot(y ~ xt, xlab = expression(x[t]), ylab = expression(y[t]))
lines(y ~ xt, lty = "dashed", lwd = 1)
lines(fitted(m1) ~ xt, lty = "solid", col = "darkolivegreen", lwd = 2)
lines(fitted(m2) ~ xt, lty = "solid", col = "red", lwd = 2)
# lines(fitted(m3$lme) ~ xt, lty = "solid", col = "midnightblue", lwd = 2)
legend("topleft",
       legend = c("Truth",
                  paste("Cubic spline (edf = ", round(m1$df, 2), ")", sep = ""),
                  paste("AM (edf = ", round(edf2, 2), ")", sep = ""),
                  paste("AM + AR(1) (edf = ", round(edf3, 2), ")", sep = "")),
       col = c("black", "darkgreen", "red", "midnightblue"),
       lty = c("dashed", rep("solid", 3)),
       lwd = c(1, rep(2, 3)),
       bty = "n", cex = 0.8)

