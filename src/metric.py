from Bio.SeqUtils import GC
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
    def __init__(self, id_human, id_species):
        self.id_human = id_human
        self.id_species = id_species
        self.coord_gene = []
        self.coord_exon= []
        self.chr=""

    def __repr__(self):
        return self.id_species + " a pour gène orthologue chez l'humain " + self.id_human

    def get_info_gene(self, filegff):
        """ 
        take a gff file (geneID human, geneID orthologue species) and return information about these geneID
        """
        formule=re.compile('\[(\d+):(\d+)\]\((.)\)')
        limit_info = dict(gff_type=["gene"])
        examiner = GFFExaminer()
        in_handle = open(filegff)
        for rec in GFF.parse(in_handle, limit_info=limit_info):
            for i in rec.features:
                texte = "GeneID:" + self.id_species
                if i.qualifiers['Dbxref'][0] == texte:
                    coordinate=formule.findall(str(i.location))
                    self.coord_gene=coordinate
                    self.chr=rec.id
        in_handle.close()

"""
    def get_info_exon(self, filegff):
        formule=re.compile('\[(\d+):(\d+)\]\((.)\)')
        limit_info = dict(gff_type=["exon"])
        examiner = GFFExaminer()
        in_handle = open(filegff)
        for rec in GFF.parse(in_handle, limit_info=limit_info):
            for i in rec.features:
                if i.type== "exon":
                    texte = "GeneID:" + self.id_species
                    if i.qualifiers['Dbxref'][0] == texte:
                        coordinate=formule.findall(str(i.location))
                        self.coord_exon.append(coordinate)
        in_handle.close()
"""



def cut_fasta_gene(dico_info_gene, fasta):
    """
    cut in a fasta file and return sequence of interess in a dico (exon, intron, gene, flanking region etc...)
    """
    dico_seq_gene = dict()
    sequence_gene = list()
    records = list(SeqIO.parse(fasta, "fasta"))
    for i in dico_info_gene.values():
        for j in i.coord_gene:
            start_gene = int(j[0])
            end_gene = int(j[1])
            strand = j[2]
        chromosome=str(i.chr)
        for fasta in records:
            if fasta.id == chromosome:
                fasta_sequence = str(fasta.seq)                     
                sequence_gene = fasta_sequence[start_gene:end_gene]
                dico_seq_gene[str(i.id_human)] = [sequence_gene, i.id_species]
    return dico_seq_gene


def calcul_GC(list_sequence_gene):
    """
    calcul GC rate from a list of sequence
    """
    taux_GC = list()
    for i in list_sequence_gene:
        test = GC(i)        
        taux_GC.append(test)
    taux_GCGene = sum(taux_GC)/len(list_sequence_gene)
    return taux_GCGene
    
def write_tab_metrics(list_metric,metrics,taxID):
    """
    take a dictionnairy of metrics dico_metric[id_humans]=(metrics) and write the metrics to the last line of an output tabulate file
    """
    if os.path.isfile('metrics_{}.txt'.format(metrics)):
        continue
    else:
         file_metric = open('metrics_{}.txt'.format(metrics),'w')
         for cle,valeur in dico_metrics.items():
             file_metric.write(cle+"\t")
             file_metric.close
    #penser au premier round où le fichier n'existe pas et où il faut écrire la première ligne!
    file_metric = open('metrics_{}.txt'.format(metrics),'a')
    file_metric.write(taxID+"\t")
    id_human=file_metric.readline()
    for human_id in id_human:
        for cle,valeur in dico_metrics.items():
            if cle==human_id:
                file.write(valeur+"\t")
            else:
                file.write("NA"+"\t")
    file_metric.close()
