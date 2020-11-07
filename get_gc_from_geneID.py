import csv
import src.metric as metric
import sys
import classSpecies


def fname(set_humain, species_dic, gffFile, fastaFile):
    """
    """
    listResult = []
    for taxid in species_dic:
        dicGene = metric.get_info_gene(species_dic[taxid], gffFile)
        sequence_genes_species = cut_fasta_gene(dicGene, fastaFile)

    for i in sequence_genes_species.values():
        if species_dic[i[2]] in species_dic:
            valeurGC = str(metric.calcul_GC(i[0]))
        else:
            valeurGC = "NA"
        listResult.append((taxid, i[2], valeurGC))
    return listResult


csvfile = open(sys.argv[1]) # CSV containing "taxid" "human_gene" "ortholog"
csv_reader = csv.DictReader(csvfile)

pathToFasta = sys.argv[2]
pathToGFF = sys.argv[3]

human_gene_set = set() # set of humans genes
species_dic = dict() # dic of object species

for row in csv_reader:
    human_gene_set.add(row["human_gene"]) # creates a set of all the available human genes
    if row["taxid"] not in species_dic: # if the species object for this taxid does not exists
        species_dic[row["taxid"]] = classSpecies.species(row["taxid"])
    species_dic[row["taxid"]].add_gene(row["human_gene"], row["geneID"]) # uses the add_gene function to add the current ortholog to the species object

