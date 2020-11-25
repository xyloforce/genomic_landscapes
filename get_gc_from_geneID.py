import csv
import src.metric as metric
import sys
import classSpecies
import src.ncbi as ncbi
import os.path

def get_metric(species_dic, gffFile, fastaFile):
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

'''
csvfile = open(sys.argv[1]) # CSV containing "taxid" "human_gene" "ortholog"
csv_reader = csv.DictReader(csvfile)
'''

csvfile = open('test.csv') # CSV containing "taxid" "human_gene" "ortholog"
csv_reader = csv.DictReader(csvfile)


human_gene_set = set() # set of humans genes
species_dic = dict() # dic of object species

for row in csv_reader:
    human_gene_set.add(row["human_gene"]) # creates a set of all the available human genes
    if row["taxid"] not in species_dic: # if the species object for this taxid does not exists
        species_dic[row["taxid"]] = classSpecies.species(row["taxid"])
    species_dic[row["taxid"]].add_gene(row["human_gene"], row["geneID"]) # uses the add_gene function to add the current ortholog to the species object



for taxid, classSpecies in species_dic.items():
   #extracted_file_list=ncbi.get_genome(taxid)
   pathToFasta="/tmp/genome/GCF_000151885.1.fna"
   pathToGFF="/tmp/genome/GCF_000151885.1.gff"
   genIDlist=dict()
   for humanid,genID in classSpecies.get_genes().items():
       genIDlist[genID[0]]=humanid
   dict_genes=metric.parsingGFF(genIDlist,pathToGFF)
   dict_genes=metric.parsing_fasta(dict_genes,pathToFasta)
   for i in dict_genes.values():
       metric.taux_GC(i)
   if not os.path.isfile('metrics_GC_gene.txt'):
       metric.create_tab_metrics(dict_genes,'GC_gene')
   metric.write_tab_metrics(dict_genes,'GC_gene',taxid)
   if not os.path.isfile('metrics_GC_exons.txt'):
       metric.create_tab_metrics(dict_genes,'GC_exons')
   metric.write_tab_metrics(dict_genes,'GC_exons',taxid)
   if not os.path.isfile('metrics_GC3_exons.txt'):
       metric.create_tab_metrics(dict_genes,'GC3_exons')
   metric.write_tab_metrics(dict_genes,'GC3_exons',taxid)
