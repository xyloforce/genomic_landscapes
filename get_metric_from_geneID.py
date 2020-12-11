import csv
import src.metric as metric
import sys
import src.classSpecies as classSpecies
import src.ncbi as ncbi
import os

#opening of the csv.
csvfile = open(sys.argv[1]) # CSV containing "taxid" "human_gene" "ortholog"
csv_reader = csv.DictReader(csvfile)

human_gene_set = set() # set of humans genes
species_dic = dict() # dic of object species

#recovery of species and associated genes.
for row in csv_reader:
    human_gene_set.add(row["human_gene"]) # creates a set of all the available human genes
    if row["taxid"] not in species_dic: # if the species object for this taxid does not exists
        species_dic[row["taxid"]] = classSpecies.species(row["taxid"])
        species_dic[row["taxid"]].set_species_name(row["species"])
    species_dic[row["taxid"]].add_gene(row["human_gene"], row["geneID"]) # uses the add_gene function to add the current ortholog to the species object

#we browse species by species
for taxid, classSpecies in species_dic.items():
   if os.path.isfile('work_done.txt'):
       exist=False
       work_done = open('work_done.txt','r')
       lignes = work_done.readlines()
       work_done.close()
       for i in lignes:
           if int(i)==int(taxid):
               print(" We already have metrics for the species {}. We move on to the next specie. ".format(classSpecies.species))
               exist=True

       if exist==True:
           continue
           
   print("download  gff and fasta files for the {} species ".format(classSpecies.species))
   #recovery of genomes in the form of fasta and gff
   try:
       extracted_file_list=ncbi.get_genome(classSpecies.species)
   except:
       print("we  not find the fasta and the gff of the complete genome of {} species, we move on to the next specie.".format(classSpecies.species))
       continue
   #verification that we have one fasta and one gff files.
   if len(extracted_file_list) != 2:
       if len(extracted_file_list)==1:
           print("the fasta or the gff is missing for the {} species. We go to the next species".format(classSpecies.species))
           os.remove(extracted_file_list[0])
           continue
       else:
           print("there is more than one fasta or gff uploaded for the {} species. We go to the next species".format(classSpecies.species))
           for i in extracted_file_list:
               os.remove(i)
           continue
   pathToFasta= extracted_file_list[1]
   pathToGFF= extracted_file_list[0]
   
   #creation of a dictionary with the human taxID as key and an info_gene object in value
   genIDlist=dict()
   for humanid,genID in classSpecies.get_genes().items():
       genIDlist[genID[0]]=humanid
   
   #parsing of the gff to get the coordinates of genes, exons and chromosomes
   print("gff parsing")
   dict_genes=metric.parsingGFF(genIDlist,pathToGFF)
   #parsing of the fasta to obtain the sequences of the genes, exons and regions, flanking
   print("fasta parsing")
   dict_genes=metric.parsing_fasta(dict_genes,pathToFasta)
   
   
   #calculation of GC rates from the sequences obtained
   for i in dict_genes.values():
       metric.taux_GC(i)
   
   #obtaining the size of the introns
   metric.get_intron_size(dict_genes)
   
   #creation of different metric files (one per metric)
   if not os.path.isfile('metrics_GC_gene.tsv'):
       metric.create_tab_metrics(human_gene_set,'GC_gene')
   metric.write_tab_metrics(dict_genes,'GC_gene',taxid)
   
   if not os.path.isfile('metrics_GC_exons.tsv'):
       metric.create_tab_metrics(human_gene_set,'GC_exons')
   metric.write_tab_metrics(dict_genes,'GC_exons',taxid)
   
   if not os.path.isfile('metrics_GC3_exons.tsv'):
       metric.create_tab_metrics(human_gene_set,'GC3_exons')
   metric.write_tab_metrics(dict_genes,'GC3_exons',taxid)
   
   if not os.path.isfile('metrics_intron_size.tsv'):
       metric.create_tab_metrics(human_gene_set,'intron_size')
   metric.write_tab_metrics(dict_genes,'intron_size',taxid)
   
   if not os.path.isfile('metrics_GC_flanking_region_before.tsv'):
       metric.create_tab_metrics(human_gene_set,'GC_flanking_region_before')
   metric.write_tab_metrics(dict_genes,'GC_flanking_region_before',taxid)
   
   if not os.path.isfile('metrics_GC_flanking_region_after.tsv'):
       metric.create_tab_metrics(human_gene_set,'GC_flanking_region_after')
   metric.write_tab_metrics(dict_genes,'GC_flanking_region_after',taxid)
   
   
   if not os.path.isfile('work_done.txt'):
       work_done = open('work_done.txt','w')
       work_done.write(str(taxid)+'\n')
       work_done.close()   
   else:
       work_done=open('work_done.txt','a')
       work_done.write(str(taxid)+'\n')
       work_done.close()
   os.remove(pathToFasta)
   os.remove(pathToGFF)

os.remove("work_done.txt")   
