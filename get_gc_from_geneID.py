import csv
#import src.metric
import sys


class species:
    def __init__(self, taxid):
        self.genes = dict()
        self.taxid = taxid

    def add_gene(self, human_gene, ortholog):
        self.genes[human_gene] = ortholog

    def __repr__(self):
        return str(len(self.genes))


csvfile = open(sys.argv[1])
csv_reader = csv.DictReader(csvfile)

human_gene_set = set()
species_dic = dict()

for row in csv_reader:
    human_gene_set.add(row["human_gene"])
    if row["taxid"] not in species_dic:
        species_dic[row["taxid"]] = species(row["taxid"])
    species_dic[row["taxid"]].add_gene(row["human_gene"], row["geneID"])
