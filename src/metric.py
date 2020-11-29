from Bio.SeqUtils import GC123
import pprint
from BCBio.GFF import GFFExaminer
from BCBio import GFF
from Bio import SeqIO
import gzip
from Bio.Alphabet import generic_dna
import re
import os.path

class info_gene(dict):
    """
    Define an object who take information about one gene.
    """
    def __init__(self, id_species):
        self.id_species = id_species
        self.genes = tuple()
        self.exons= dict()
        self.chr=""
        self.seq_gene=""
        self.sequence_flanquante_avant=""
        self.sequence_flanquante_apres=""
        self.sequence_exon=list()
        self.taux_GC_gene= str()
        self.taux_GC_exon=str()
        self.taux_GC3_exon=str()
        self.taille_intron=str()
        self.taux_GC_flanquante_avant=str()
        self.taux_GC_flanquante_apres=str()
    def __repr__(self):
        return "le gene est le "+ self.id_species+ " qui va de " + str(self.genes[0]) + " à "+ str(self.genes[1]) + " sur le  chromosome " + str(self.chr)

    def get_genes(self):
        return self.genes
       
    def get_exons(self):
        return self.exons

    def get_chromosome(self):
        return self.chr
       
    def set_exons(self,exons):
        self.exons.update(exons)
      
    def set_genes(self,genes):
        self.genes=genes

    def set_chromosome(self, chromosome):
        self.chr=chromosome

    def set_sequence_gene(self,seq_gene):
        self.seq_gene=seq_gene

    def set_sequence_exon(self, sequence_exon):
        self.sequence_exon.append(sequence_exon)
        
    def set_taille_intron(self,taille_intron):
        self.taille_intron=taille_intron

    def set_sequence_fanquante_avant(self,sequence):
        self.sequence_flanquante_avant=sequence

    def set_sequence_fanquante_apres(self,sequence):
        self.sequence_flanquante_apres=sequence


def get_intron_size(dict_gene):
    for gene in dict_gene.values():
        # calculating introns size
        list_taille_exons = []
        taille_gene= abs(int(gene.genes[1])-int(gene.genes[0]))
        for exon in gene.exons.values():
            taille_One_exon=abs(int(exon[1])-int(exon[0]))
            list_taille_exons.append(taille_One_exon)
        taille_exons=sum(list_taille_exons)
        taille_intron=taille_gene-taille_exons
        if taille_intron<0:
            taille_intron='NA'
        gene.set_taille_intron(str(taille_intron))

	
def parsingGFF(dico_geneID, fileGFF):
    """
    Get start and stop exon from GFF file.

    IN: GFF and a gene ID list
    OUT: dict[geneID] = [(exon start, exon stop)…]
    """
    geneID=list()
    for i in dico_geneID.keys():
        geneID.append(i)
    def inGene(geneID, limitDown, limitUp):
        if limitDown >= dict_info_gene[humanid].genes[0] and limitUp <= dict_info_gene[humanid].genes[1]:
            return True
        return False
    dict_info_gene=dict()
    limitsGenes = {}
    with open(fileGFF, 'r') as file:
        regex = "(^.*)\t.*\t(exon|gene).(\d+).(\d+).+GeneID:(\d+)"
        # group :: 1 chromosome 2 exon/gene 3 start ; 4 stop ; 5 GeneID
        for line in file:
            if line[0] == '#':
                continue
            match = re.search(regex, line)
            if match is None:
                continue
            if match.group(5) in geneID:
                # geneID found by get_orthologs
                humanid=dico_geneID[match.group(5)]
                if humanid not in dict_info_gene:
                    dict_info_gene[humanid]=info_gene(match.group(5))
                    dict_info_gene[humanid].set_chromosome(match.group(1))
                if match.group(2) == "gene":
                    tuple_gene=(match.group(3), match.group(4))
                    dict_info_gene[humanid].set_genes(tuple_gene)
                if match.group(2) == "exon":
                    exons={}
                    try:
                        # test if exon in gene limit
                        if inGene(match.group(5), match.group(3), match.group(4)):
                            # get numero of exon
                            exonID = re.search("ID=exon-.+-(\d+);", line)
                            if exonID is None:
                                print(f"No ID exon found for gene {match.group(5)}")
                            exons[int(exonID.group(1))] = (int(match.group(3)), int(match.group(4)))
                            dict_info_gene[humanid].set_exons(exons)
                    except Exception as e:
                        print(e)
    return dict_info_gene





def parsing_fasta(dico_info_gene, fasta):
    #parsage du fasta
    records = list(SeqIO.parse(fasta, "fasta"))
    
    #parcours des objets info_gene
    for info_gene in dico_info_gene.values():
        for fasta in records:
        
            #ne prendre que la séquence fasta qui nous intéresse
            if fasta.id == info_gene.chr:
            
                #transformer la sequence fasta en une chaine de caractère
                fasta_sequence = str(fasta.seq)
                
                #récupération séquence du gène
                start_gene= int(info_gene.genes[0])
                end_gene= int(info_gene.genes[1])
                sequence_gene = fasta_sequence[start_gene:end_gene]
                info_gene.set_sequence_gene(sequence_gene)
                
                #récupération séquence région flanquante avant le gène
                limite_flanking_avant=start_gene-5000
                if limite_flanking_avant<0:
                    limite_flanking_avant=0
                sequence_flanking_avant=fasta_sequence[limite_flanking_avant:start_gene]
                info_gene.set_sequence_fanquante_avant(sequence_flanking_avant)
                
                #récupération séquence région flanquante après le gène
                limite_flanking_apres=end_gene + 5000
                if limite_flanking_apres>len(fasta_sequence):
                    limite_flanking_apres=len(fasta_sequence)
                sequence_flanking_apres=fasta_sequence[end_gene:limite_flanking_apres]
                info_gene.set_sequence_fanquante_apres(sequence_flanking_apres)
                
                #récupération séquence des exons
                for i in info_gene.exons.values():
                    start_exon=int(i[0])
                    end_exon=int(i[1])
                    fasta_sequence = str(fasta.seq)
                    sequence_exon = fasta_sequence[start_exon:end_exon]
                    info_gene.set_sequence_exon(sequence_exon)
    return dico_info_gene

def calcul_GC(list_sequence_gene,type_GC):
    """
    calcul GC rate from a list of sequence
    """
    taux_GC = list()
    if len(list_sequence_gene)==0:
        taux_GCGene='NA'
        return taux_GCGene
    for i in list_sequence_gene:
        if len(i)==0:
            continue
        test = GC123(i)
        test= test[int(type_GC)]
        taux_GC.append(test)
    taux_GCGene = sum(taux_GC)/len(list_sequence_gene)
    return taux_GCGene

def taux_GC(objet):
    list_seq_gene=[objet.seq_gene]
    objet.taux_GC_gene=calcul_GC(list_seq_gene,0)
    
    
    objet.taux_GC_exon=calcul_GC(objet.sequence_exon,0)
    objet.taux_GC3_exon=calcul_GC(objet.sequence_exon,3)
    
    list_seq_flanquante_avant=[objet.sequence_flanquante_avant]
    objet.taux_GC_flanquante_avant=calcul_GC(list_seq_flanquante_avant,0)
    
    list_seq_flanquante_apres=[objet.sequence_flanquante_apres]
    objet.taux_GC_flanquante_apres=calcul_GC(list_seq_flanquante_apres,0)


def create_tab_metrics(set_human_gene,metrics):
    file_metric = open('metrics_{}.txt'.format(metrics),'w')
    file_metric.write("genome reference"+"\t")
    for humanID in set_human_gene:
        file_metric.write(str(humanID)+"\t")
    file_metric.write("\n")
    file_metric.close


def write_tab_metrics(dico_metric,metrics,taxID):
    """
    take a dictionnairy of metrics dico_metric[id_humans]=(metrics) and write the metrics to the last line of an output tabulate file
    """
    read_metric=open('metrics_{}.txt'.format(metrics),'r')
    id_human=read_metric.readline()
    read_metric.close()
    id_human=id_human.split('\t')
    del id_human[-1]
    print(id_human)
    print(len(id_human))
    file_metric_2 = open('metrics_{}.txt'.format(metrics),'a')
    file_metric_2.write(taxID+"\t")
    for index,human_id in enumerate(id_human):
        if index==0:
            continue
        aucune_ecriture=True
        for cle,valeur in dico_metric.items():
            if cle==human_id:
                if metrics=='GC_gene':
                    file_metric_2.write(str(valeur.taux_GC_gene)+"\t")
                    aucune_ecriture=False
                    continue
                if metrics=='GC_exons':
                    file_metric_2.write(str(valeur.taux_GC_exon)+"\t")
                    aucune_ecriture=False
                    continue
                if metrics=='GC3_exons':
                    file_metric_2.write(str(valeur.taux_GC3_exon)+"\t")
                    aucune_ecriture=False
                    continue
                if metrics=='taille_intron':
                     file_metric_2.write(str(valeur.taille_intron)+"\t")
                     aucune_ecriture=False
                     continue
                if metrics=='taux_GC_flanquante_avant':
                    file_metric_2.write(str(valeur.taux_GC_flanquante_avant)+"\t")
                    aucune_ecriture=False
                    continue
                if metrics=='taux_GC_flanquante_apres':
                    file_metric_2.write(str(valeur.taux_GC_flanquante_apres)+"\t")
                    aucune_ecriture=False
                    continue
        if aucune_ecriture==True:
            file_metric_2.write("NA"+"\t")
            test=False                         
    file_metric_2.write("\n")
    file_metric_2.close()
