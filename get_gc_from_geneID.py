import csv
import src.metric as metric
import sys


class species:
    def __init__(self, taxid):
        self.genes = dict()
        self.taxid = taxid

    def add_gene(self, human_gene, ortholog):
        self.genes[human_gene] = ortholog

    def __repr__(self):
        return str(len(self.genes))


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


csvfile = open(sys.argv[1])
csv_reader = csv.DictReader(csvfile)

pathToFasta = sys.argv[2]
pathToGFF = sys.argv[2]

human_gene_set = set() # set of humans genes
species_dic = dict() # dic of object species

for row in csv_reader:
    human_gene_set.add(row["human_gene"])
    if row["taxid"] not in species_dic:
        species_dic[row["taxid"]] = species(row["taxid"])
    species_dic[row["taxid"]].add_gene(row["human_gene"], row["geneID"])
