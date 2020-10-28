from Bio.SeqUtils import GC
import pprint
from BCBio.GFF import GFFExaminer
from BCBio import GFF
from Bio import SeqIO
import gzip
from Bio.Alphabet import generic_dna


class info_gene(dict):
    def __init__(self, id_human, id_species, start, end, strand):
        self.id_human = id_human
        self.id_species = id_species
        self.start = start
        self.end = end
        self.strand = strand

    def __repr__(self):
        return self.id_species + " a pour gène orthologue chez l'humain " + self.id_human


in_file = "subset500_GCF_GRCh38.gff"
test = [("id_humain_1", "102466751"),
        ("id_humain_2", "107985721"),
        ("id_humain_3", "79854")]


def get_info_gene(liste_tuple_gene, filegff):
    dico_info_gene = dict()
    for tuple_gene in liste_tuple_gene:
        limit_info = dict(gff_type=["gene"])
        examiner = GFFExaminer()
        in_handle = open(filegff)
        for rec in GFF.parse(in_handle, limit_info=limit_info):
            for i in rec.features:
                texte = "GeneID:" + tuple_gene[1]
                if i.qualifiers['Dbxref'][0] == texte:
                    localisation = str(i.location)
                    localisation = localisation.split('](')
                    localisation[0] = localisation[0][1:]
                    localisation[1] = localisation[1][:-1]
                    localisation[0] = localisation[0].split(':')
                    info = info_gene(id_human=tuple_gene[0],
                                     id_species=tuple_gene[1],
                                     start=localisation[0][0],
                                     end=localisation[0][1],
                                     strand=localisation[1])
                    dico_info_gene[info.id_species] = info
                in_handle.close()
            return dico_info_gene


def cut_fasta_gene(dico_info_gene, fasta):
    dico_seq_fasta = dict()
    sequence_gene = list()
    records = list(SeqIO.parse(fasta, "fasta"))
    fasta_sequence = str(records[0].seq)
    for i in dico_info_gene.values():
        start_gene = int(i.start)
        end_gene = int(i.end)
        strand = i.strand
        nom_gene = i.id_species
        sequence_gene = fasta_sequence[start_gene:end_gene]
        dico_seq_fasta[str(i.id_human)] = [sequence_gene, nom_gene, i.id_human]
    return dico_seq_fasta


fasta = "test.fna"


def calcul_GC(list_sequence_gene):
    taux_GC = list()
    for i in list_sequence_gene:
        test = GC(i)
        taux_GC.append(test)
    taux_GCGene = sum(taux_GC)/len(list_sequence_gene)
    return taux_GCGene


dico = get_info_gene(test, in_file)
sequence_genes_specie = cut_fasta_gene(dico, fasta)


for i in sequence_genes_specie.values():
    test = str(calcul_GC(i[0]))
    print("le gène "+i[1] + " qui est orthologue du gène " + i[2] + " dans le génome de référence à un taux de GC de " + test + " %")
