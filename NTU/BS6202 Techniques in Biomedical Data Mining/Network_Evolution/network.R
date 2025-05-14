library(org.Hs.eg.db)
library(clusterProfiler)
library(GOSemSim)
library(clusterProfiler)
library(stringr)
# bitr(human_all, fromType="UNIPROT", toType="ENTREZID", OrgDb="org.Hs.eg.db", drop = TRUE)
# bitr(human_all, fromType="UNIPROT", toType="ENTREZID", OrgDb="org.Hs.eg.db", drop = TRUE)

setwd("~/id conversion")

hsGO <- godata('org.Hs.eg.db', ont="MF") 
human_all <- as.list(read.table("human_all.txt"))$V1
human_conserved <- as.list(read.table("human_conserved_ID.txt"))$V1
human_specific <- as.list(read.table("human_specific_ID.txt"))$V1
GOSemSim::clusterSim(human_conserved, human_specific, semData=hsGO, measure="Jiang", combine="BMA")
DOSE::clusterSim(human_conserved, human_specific, measure="Jiang", combine="BMA")

library(org.Sc.sgd.db)
ScGO <- godata('org.Sc.sgd.db', ont="MF") 
library(enrichplot)

ego <- enrichGO(gene          = human_conserved,
                universe      = names(human_all),
                OrgDb         = org.Hs.eg.db,
                ont           = "ALL",
                pAdjustMethod = "BH",
                pvalueCutoff  = 0.05,
                qvalueCutoff  = 0.05,
                readable      = TRUE)
head(ego)
library(ggplot2)
dotplot(ego, showCategory=20) + ggtitle("Human conserved protein GO enrichment")+theme(axis.text=element_text(size=1), axis.text.y = element_text(color = "grey20", size = 7, angle = 0, hjust = 1, vjust = 0, face = "plain"))+scale_y_discrete(labels=function(x) str_wrap(x, width=30))+xlim(0,.25)



human_specific_ego <- enrichGO(gene          = human_specific,
                universe      = names(human_specific),
                OrgDb         = org.Hs.eg.db,
                ont           = "ALL",
                pAdjustMethod = "BH",
                pvalueCutoff  = 0.05,
                qvalueCutoff  = 0.05,
                readable      = TRUE)
head(human_specific_ego)
library(ggplot2)
dotplot(human_specific_ego, showCategory=20) + ggtitle("Human specific protein GO enrichment")

edo <- pairwise_termsim(human_specific_ego)
p1 <- emapplot(edo)
p2 <- emapplot(edo, cex_category=1.5)
p3 <- emapplot(edo, layout="kk", cex_category=0.3)
p4 <- emapplot(edo, cex_category=1.5,layout="kk") 
cowplot::plot_grid(p1, p2, p3, p4, ncol=2, labels=LETTERS[1:4])
  theme(axis.text=element_text(size=1), 
        axis.text.y = element_text(color = "grey20", 
                                   size = 7, 
                                   angle = 0, 
                                   hjust = 1, 
                                   vjust = 0, 
                                   face = "plain"))

  
p3 <- emapplot(edo, layout="kk", cex_category=0.5, cex_label_category=0.5)
p3


edo <- pairwise_termsim(ego)
p1 <- emapplot(edo)
p2 <- emapplot(edo, cex_category=1.5)
p3 <- emapplot(edo, layout="kk", cex_category=0.3)
p4 <- emapplot(edo, cex_category=1.5,layout="kk") 
cowplot::plot_grid(p1, p2, p3, p4, ncol=2, labels=LETTERS[1:4])
theme(axis.text=element_text(size=1), 
      axis.text.y = element_text(color = "grey20", 
                                 size = 7, 
                                 angle = 0, 
                                 hjust = 1, 
                                 vjust = 0, 
                                 face = "plain"))


p3 <- emapplot(edo, layout="kk", cex_category=0.5, cex_label_category=0.5)
p3

