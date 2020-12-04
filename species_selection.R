library(ggplot2)
library(dplyr)
length_uniq <- function(x) {
  return (length(unique(x)))
}

species_gene_humanortho <- read.csv("species_gene_humanortho.csv")
species_gene_humanortho[species_gene_humanortho$species == "Monachus schauinslandi", 2] <- "Neomonachus schauinslandi" # same thing : see https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=29088
taxo_reference <- read.csv("taxo_reference.csv", header=FALSE, sep=",", fill = TRUE)
speciesbygenre = aggregate(x = taxo_reference$V1, by = list(taxo_reference$V13), FUN=length) # tweak this parameter to find optimal level

###### first sort by genre + percent of unique orthologs #####
orthologs_by_species=aggregate(species_gene_humanortho$human_gene, by=list(species_gene_humanortho$species), FUN=length_uniq) # human gene: number of hits by species by gene
orthologs_by_species$percent = orthologs_by_species$x/length(unique(species_gene_humanortho$human_gene))*100 # get percent of human genes with orthologs

orthologs_by_species$genre = taxo_reference[match(taxo_reference$V1, orthologs_by_species$Group.1),13] # add genre info

orthologs_by_species = orthologs_by_species[order(orthologs_by_species$genre, orthologs_by_species$percent, decreasing = TRUE),] # sort by genre and percent human genes
selected_species = orthologs_by_species[match(speciesbygenre$Group.1, orthologs_by_species$genre),] # select only the first species of each genre
selected_species = rbind(selected_species, orthologs_by_species[(orthologs_by_species$genre == "" & !(orthologs_by_species$Group.1 %in% selected_species$Group.1)),]) # add species with no genre for max diversity

genes_valides=species_gene_humanortho[species_gene_humanortho$species %in% selected_species$Group.1,] # keep only these genes
genes_valides$concat=paste(genes_valides$human_gene, genes_valides$taxid) # create an ID to filter
genes_uniques= genes_valides %>% group_by(concat) %>% sample_n(1) # keep a sample of size one for each ID created before

final_output=genes_uniques[,c("species", "taxid", "human_gene", "geneID")]
write.csv(final_output, "results.csv", row.names = FALSE)