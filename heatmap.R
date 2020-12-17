#!/usr/bin/env Rscript
# This script is to be run with Rscript and given as args
# 1 the name of the file to be filtered
# 2 the name of the taxofile
# 3 the name of the geneinfo file
# 4 the name of the output png
# 5 and the graph title
args = commandArgs(trailingOnly=TRUE)

# Load data
metrics2 = read.csv(args[1], na.strings="NA", check.names=FALSE, stringsAsFactors = FALSE, sep="\t", row.names = 1)
# delete full NA rows / columns
metrics2 <- metrics2[,colSums(is.na(metrics2))<nrow(metrics2)]
metrics2 =  metrics2[rowSums(is.na(metrics2)) != ncol(metrics2), ]
# load supplementary file : taxo_reference (infos on species)
taxo_reference = read.csv(args[2], header=FALSE)
# use the file to rename rows by species names instead of taxid
row.names(metrics2) = taxo_reference[match(row.names(metrics2),taxo_reference$V2),1]
# load supplementary file : gene_infos.csv (infos on human genome)
gene_infos <- read.csv(args[3], header=FALSE, stringsAsFactors = FALSE)
# use the file to rename rows by gene symbol
colnames(metrics2) = gene_infos[match(colnames(metrics2), as.character(gene_infos$V1)),2]
# then to sort genes by pos on chromosome
metrics2 = metrics2[,order(gene_infos[match(colnames(metrics2),gene_infos$V2),3], gene_infos[match(colnames(metrics2),gene_infos$V2),4])]
colors = colorRampPalette(c("blue", "white", "red"))
# make a label list to indicate which chromosom is displayed
labelCols = gene_infos[match(colnames(metrics2), gene_infos$V2),3]
# print the heatmap
png(filename = args[4], width=1920, height=1080)
heatmap(data.matrix(metrics2), Colv = NA, col = colors(100), labCol = labelCols)
# add ylab (badly positionned by default)
mtext(args[5], side = 1, line = 3, font = 2, cex=1.5)
mtext("Espèces", side=2, line=0)
mtext("Chromosomes", side=1, line=2)
legend("bottomleft", legend=c(round(min(as.matrix(metrics2), na.rm=TRUE), digits=2), round(mean(as.matrix(metrics2), na.rm=TRUE), digits=2), round(max(as.matrix(metrics2), na.rm=TRUE), digits = 2)), fill=colors(3))
dev.off()

