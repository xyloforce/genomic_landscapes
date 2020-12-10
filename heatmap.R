library(ggplot2)
library(reshape2)
library(ggdark)

metrics = read.csv("Metrics/metrics_GC3_exons.txt", na.strings="NA", check.names=FALSE, stringsAsFactors = FALSE, sep="\t")
taxo_reference = read.csv("taxo_reference.csv", header=FALSE)
taxo_reference$taxo = do.call(paste, c(taxo_reference[,3:19], sep="-"))
colnames(metrics)[1] = "taxid" # because that's a motherfucking taxid
metrics$taxid = paste("t", metrics$taxid, sep = "_")
ggplot2_rdy = melt(metrics, id = c("taxid"))
gene_infos <- read.csv("gene_infos.csv", header=FALSE, stringsAsFactors = FALSE)

ggplot2_rdy$taxo = taxo_reference[match(ggplot2_rdy$taxid,paste("t", taxo_reference$V2, sep = "_")),20]
ggplot2_rdy$species.name = taxo_reference[match(ggplot2_rdy$taxid,paste("t", taxo_reference$V2, sep = "_")),1]

ggplot2_rdy[c("gene_symbol", "chromosome", "start")] = gene_infos[match(ggplot2_rdy$variable, gene_infos$V1), 2:4]
ggplot2_rdy = ggplot2_rdy[order(ggplot2_rdy$chromosome, ggplot2_rdy$start),]
ggplot2_rdy$species.name = with(ggplot2_rdy, reorder(species.name, order(ggplot2_rdy$taxo))) # reorder species according to species
ggplot2_rdy$gene_symbol = with(ggplot2_rdy, reorder(gene_symbol, order(ggplot2_rdy$chromosome, ggplot2_rdy$start))) # reorder gene_symbol by chromosome and start pos

ggplot(data = ggplot2_rdy, aes(x=gene_symbol, y=species.name)) + geom_tile(aes(fill = value)) + scale_fill_gradient2(low = "#19ABFA", high = "#FA0011", mid = "white",  midpoint = median(ggplot2_rdy$value, na.rm = TRUE), limit = quantile(ggplot2_rdy$value, probs = c(0.05,0.95), na.rm = TRUE)) + scale_x_discrete("Chromosoms", breaks = ggplot2_rdy[match(sort(unique(gene_infos$V3)), ggplot2_rdy$chromosome),"gene_symbol"], labels = sort(unique(gene_infos$V3)))
