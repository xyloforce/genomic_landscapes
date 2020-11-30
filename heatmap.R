library(ggplot2)
library(reshape2)
library(ggdark)

alexandria = read.csv("~/Documents/Cours/3_M2/Projet/alexandria.csv", na.strings="Na", check.names=FALSE, stringsAsFactors = FALSE)
alexandria$taxid = paste("t", alexandria$taxid, sep = "_")
ggplot2_rdy = melt(alexandria, id = c("taxid"))
gene_infos <- read.csv("~/Documents/Cours/3_M2/Projet/gene_infos.csv", header=FALSE, stringsAsFactors = FALSE)

ggplot2_rdy[c("gene_symbol", "chromosome", "start")] = gene_infos[match(ggplot2_rdy$variable, gene_infos$V1), 2:4]
ggplot2_rdy = ggplot2_rdy[order(ggplot2_rdy$chromosome, ggplot2_rdy$start),]

ggplot2_rdy$gene_symbol = with(ggplot2_rdy, reorder(gene_symbol, order(ggplot2_rdy$chromosome, ggplot2_rdy$start)))

ggplot(data = ggplot2_rdy, aes(x=gene_symbol, y=taxid)) + geom_tile(aes(fill = value)) + scale_fill_gradient2(low = "#19ABFA", high = "#FA0011", mid = "white",  midpoint = median(ggplot2_rdy$value, na.rm = TRUE), limit = quantile(ggplot2_rdy$value, probs = c(0.05,0.75), na.rm = TRUE)) + scale_x_discrete("Chromosoms", breaks = ggplot2_rdy[match(sort(unique(gene_infos$V3)), ggplot2_rdy$chromosome),4], labels = sort(unique(gene_infos$V3)))
