#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

# Load data
metrics2 = read.csv(args[1], na.strings="NA", check.names=FALSE, stringsAsFactors = FALSE, sep="\t", row.names = 1)
# delete full NA rows / columns
metrics2 <- metrics2[,colSums(is.na(metrics2))<nrow(metrics2)]
metrics2 =  metrics2[rowSums(is.na(metrics2)) != ncol(metrics2), ]
# load supplementary file : taxo_reference (infos on species)
taxo_reference = read.csv("taxo_reference.csv", header=FALSE)
# use the file to rename rows by species names instead of taxid
row.names(metrics2) = taxo_reference[match(row.names(metrics2),taxo_reference$V2),1]
# load supplementary file : gene_infos.csv (infos on human genome)
gene_infos <- read.csv("gene_infos.csv", header=FALSE, stringsAsFactors = FALSE)
# use the file to rename rows by gene symbol
colnames(metrics2) = gene_infos[match(colnames(metrics2), as.character(gene_infos$V1)),2]
# then to sort genes by pos on chromosome
metrics2 = metrics2[,order(gene_infos[match(colnames(metrics2),gene_infos$V2),3], gene_infos[match(colnames(metrics2),gene_infos$V2),4])]
colors = colorRampPalette(c("blue", "white", "red"))
# make a label list to indicate which chromosom is displayed
labelCols = gene_infos[match(colnames(metrics2), gene_infos$V2),3]
# print the heatmap
heatmap(data.matrix(metrics2), Colv = NA, col = colors(100), labCol = labelCols, xlab = "Chromosomes", main = args[2])
# add ylab (badly positionned by default)
mtext("Espèces", side=2, line=0)

