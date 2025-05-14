library(robvis)
library(openxlsx)

Dataset <- read.xlsx('Dataset_version_latest.xlsx', 'Combined') 

pdf('RoB_barplot.pdf', width = 9, height = 3.2)
rob_data <- unique(Dataset[c('Study.Identifier','Domain.1','Domain.2','Domain.3','Domain.4','Domain.5','Overall')])
rob_summary(rob_data, tool = "ROB2", weighted = FALSE)
dev.off()

pdf('RoB_taffic.pdf', width = 7, height = 9)
rob_traffic_light(rob_data, tool = "ROB2", psize = 5)
dev.off()

rob_data.2022 <- unique(Dataset[Dataset$'Source' == '2022 search', ][c('Study.Identifier','Domain.1','Domain.2','Domain.3','Domain.4','Domain.5','Overall')])
rob_data.2019 <- unique(Dataset[Dataset$'Source' != '2022 search', ][c('Study.Identifier','Domain.1','Domain.2','Domain.3','Domain.4','Domain.5','Overall')])

pdf('RoB_taffic_2019.pdf', width = 7, height = 9)
rob_traffic_light(rob_data.2019, tool = "ROB2", psize = 5)
dev.off()

pdf('RoB_taffic_2022.pdf', width = 7, height = 4.5)
rob_traffic_light(rob_data.2022, tool = "ROB2", psize = 5)
dev.off()

pdf('RoB_barplot_2019.pdf', width = 9, height = 3.2)
rob_summary(rob_data.2019, tool = "ROB2", weighted = FALSE)
dev.off()

pdf('RoB_barplot_2022.pdf', width = 9, height = 3.2)
rob_summary(rob_data.2022, tool = "ROB2", weighted = FALSE)
dev.off()