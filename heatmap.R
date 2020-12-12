metrics2 = read.csv("Metrics/metrics_GC_flanking_region_before.tsv", na.strings="NA", check.names=FALSE, stringsAsFactors = FALSE, sep="\t", row.names = 1)
metrics2 <- metrics2[,colSums(is.na(metrics2))<nrow(metrics2)]
metrics2 =  metrics2[rowSums(is.na(metrics2)) != ncol(metrics2), ]
taxo_reference = read.csv("taxo_reference.csv", header=FALSE)
row.names(metrics2) = taxo_reference[match(row.names(metrics2),taxo_reference$V2),1]
gene_infos <- read.csv("gene_infos.csv", header=FALSE, stringsAsFactors = FALSE)
colnames(metrics2) = gene_infos[match(colnames(metrics2), as.character(gene_infos$V1)),2]
metrics2 = metrics2[,order(gene_infos[match(colnames(metrics2),gene_infos$V2),3], gene_infos[match(colnames(metrics2),gene_infos$V2),4])]
colors = colorRampPalette(c("blue", "white", "red"))

labelCols = gene_infos[match(colnames(metrics2), gene_infos$V2),3]
heatmap(data.matrix(metrics2), Colv = NA, col = colors(100), labCol = labelCols, xlab = "Chromosomes", main = "Taux de GC des régions flanquantes amont par espèce")
mtext("Espèces", side=2, line=0)

