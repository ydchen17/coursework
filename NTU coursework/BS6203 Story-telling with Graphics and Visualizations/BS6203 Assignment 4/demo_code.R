# Library
library(viridis)
library(readxl)
library(reshape2)
library(plotly)

# Data transformation
data <- t(read_excel("Data_waiting-times.xls", skip = 1))
colnames(data) <- data[1,]
data<-data[-1,]
data<-melt(data)
data<-data[-57,]
colnames(data)<-c("Hospital","Date","WaitingTime")
data$WaitingTime<-as.numeric(data$WaitingTime)
data$Date<-as.Date(data$Date)

# Factor reorder
#levels(data$Hospital)
orders <- reorder (data$Hospital, data$WaitingTime)
data$Hospital <- factor(data$Hospital, levels = rev(levels(orders)))
#orders <- c("KTPH","AH","NUH(A)","NTFGH","SGH","SKH","TTSH","CGH")
#data$Hospital<- factor(data$Hospital, levels = rev(orders))

# Plotting
p <- ggplot(data,
            aes(x=Date, 
                y=WaitingTime, 
                group=Hospital,
                fill=Hospital)
) + 
  geom_area(alpha=0.6 , size=.5, colour="white") +
  scale_fill_viridis(discrete = T) +
  theme_light()+
  xlab("Date") + 
  ylab("Median Wait Time for Admission at ED (Hr)")+
  ggtitle("Statistics of wait time for admission to ward\n (Sun 25 - Sat 31 Oct 2020)")
# non-interactive visualisation 
#p
# interactive visualisation 
ggplotly(p)