#!/usr/bin/env Rscript
# This script is to be run with Rscript and given as arg :
#1 the name of the file to be filtered
#2 the name of the taxo reference file
#3 if the user wishes to select a random sample for each duplicate or remove them from analysis
#args = commandArgs(trailingOnly=TRUE)
args = c("species_gene_humanortho.csv", "taxo_reference.csv", 0)

library(dplyr)
length_uniq <- function(x) {
  return (length(unique(x)))
}

species_gene_humanortho <- read.csv(args[1]) # select file given as arg
species_gene_humanortho[species_gene_humanortho$species == "Monachus schauinslandi", 2] <- "Neomonachus schauinslandi" # same thing : see https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=29088
taxo_reference <- read.csv(args[2], header=FALSE, sep=",", fill = TRUE)
speciesbygenre = aggregate(x = taxo_reference$V1, by = list(taxo_reference$V13), FUN=length) # tweak this parameter to find optimal level

orthologs_by_species=aggregate(species_gene_humanortho$human_gene, by=list(species_gene_humanortho$species), FUN=length_uniq) # human gene: number of hits by species by gene
orthologs_by_species$percent = orthologs_by_species$x/length(unique(species_gene_humanortho$human_gene))*100 # get percent of human genes with orthologs

orthologs_by_species$genre = taxo_reference[match(taxo_reference$V1, orthologs_by_species$Group.1),13] # add genre info

orthologs_by_species = orthologs_by_species[order(orthologs_by_species$genre, orthologs_by_species$percent, decreasing = TRUE),] # sort by genre and percent human genes
selected_species = orthologs_by_species[match(speciesbygenre$Group.1, orthologs_by_species$genre),] # select only the first species of each genre
selected_species = rbind(selected_species, orthologs_by_species[(orthologs_by_species$genre == "" & !(orthologs_by_species$Group.1 %in% selected_species$Group.1)),]) # add species with no genre for max diversity

genes_valides=species_gene_humanortho[species_gene_humanortho$species %in% selected_species$Group.1,] # keep only these genes
# either the user wants no duplicated genes either he wants one of them
genes_valides$concat=paste(genes_valides$human_gene, genes_valides$taxid) # create an ID to filter
if(args[3]==1) {
  genes_uniques= genes_valides %>% group_by(concat) %>% sample_n(1) # keep a sample of size one for each ID created before
} else {
  num_ids = aggregate(genes_valides$concat, by=list(genes_valides$human_gene), FUN=length)
  genes_uniques = genes_valides[num_ids[match(genes_valides$geneID, num_ids$Group.1)==1,2]==1,]
}
final_output=genes_uniques[,c("species", "taxid", "human_gene", "geneID")]
write.csv(final_output, "results.csv", row.names = FALSE)
