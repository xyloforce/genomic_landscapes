import csv
import src.metric as metric
import sys
import classSpecies
import src.ncbi as ncbi
import os.path


#ouverture du csv
csvfile = open(sys.argv[1]) # CSV containing "taxid" "human_gene" "ortholog"
csv_reader = csv.DictReader(csvfile)




human_gene_set = set() # set of humans genes
species_dic = dict() # dic of object species

#récupération des espèces et des gènes associés.
for row in csv_reader:
    human_gene_set.add(row["human_gene"]) # creates a set of all the available human genes
    if row["taxid"] not in species_dic: # if the species object for this taxid does not exists
        species_dic[row["taxid"]] = classSpecies.species(row["taxid"])
    species_dic[row["taxid"]].add_gene(row["human_gene"], row["geneID"]) # uses the add_gene function to add the current ortholog to the species object

print(human_gene_set)
print(len(human_gene_set))

#on parcours espèce par espèce
for taxid, classSpecies in species_dic.items():
   #récupération des génomes sous forme de fasta et de gff
   extracted_file_list=ncbi.get_genome(taxid)
   pathToFasta= extracted_file_list[0]
   pathToGFF= extracted_file_list[1]
   
   #création d'un dictionnaire avec comme clé les taxID huamin et en valeur un objet info_gene.
   genIDlist=dict()
   for humanid,genID in classSpecies.get_genes().items():
       genIDlist[genID[0]]=humanid
       
   #parsing du gff et du fasta pour obtenir les coordonnées des gènes, exons et les chromosomes
   dict_genes=metric.parsingGFF(genIDlist,pathToGFF)
   dict_genes=metric.parsing_fasta(dict_genes,pathToFasta)
   
   
   #calcul des taux de GC
   for i in dict_genes.values():
       metric.taux_GC(i)
   
   #obtention de la taille des introns
   metric.get_intron_size(dict_genes)
   
   #création des différents fichiers de métrique (un par métrique)
   if not os.path.isfile('metrics_GC_gene.txt'):
       metric.create_tab_metrics(human_gene_set,'GC_gene')
   metric.write_tab_metrics(dict_genes,'GC_gene',taxid)
   if not os.path.isfile('metrics_GC_exons.txt'):
       metric.create_tab_metrics(human_gene_set,'GC_exons')
   metric.write_tab_metrics(dict_genes,'GC_exons',taxid)
   if not os.path.isfile('metrics_GC3_exons.txt'):
       metric.create_tab_metrics(human_gene_set,'GC3_exons')
   metric.write_tab_metrics(dict_genes,'GC3_exons',taxid)
   if not os.path.isfile('metrics_taille_intron.txt'):
       metric.create_tab_metrics(human_gene_set,'taille_intron')
   metric.write_tab_metrics(dict_genes,'taille_intron',taxid) 
   if not os.path.isfile('metrics_taux_GC_flanquante_avant.txt'):
       metric.create_tab_metrics(human_gene_set,'taux_GC_flanquante_avant')
   metric.write_tab_metrics(dict_genes,'taux_GC_flanquante_avant',taxid)     
   if not os.path.isfile('metrics_taux_GC_flanquante_apres.txt'):
       metric.create_tab_metrics(human_gene_set,'taux_GC_flanquante_apres')
   metric.write_tab_metrics(dict_genes,'taux_GC_flanquante_apres',taxid)   
      
   
   
   






