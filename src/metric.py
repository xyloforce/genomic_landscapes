from Bio.SeqUtils import GC
import pprint
from BCBio.GFF import GFFExaminer
from BCBio import GFF

class info_gene(dict):
	def __init__(self, id_human, id_species,start,end,strand):
	        self.id_human = id_human
	        self.id_species = id_species
	        self.start=start
	        self.end=end
	        self.strand=strand
	def __repr__(self):
        	return self.id_species + " a pour gène orthologue chez l'humain "+ self.id_human



in_file = "subset500_GCF_GRCh38.gff"
test=[("id_humain_1","102466751"),("id_humain_2","107985721"),("id_humain_3","79854")]

def get_info_gene(liste_tuple_gene,filegff):
	dico_info_gene=dict()
	for j in liste_tuple_gene:
		limit_info = dict( gff_type=["gene"])
		examiner = GFFExaminer()
		in_handle = open(filegff)
		for rec in GFF.parse(in_handle, limit_info=limit_info):
			for i in rec.features:
				texte="GeneID:"+j[1]
				if i.qualifiers['Dbxref'][0]==texte:
					localisation=str(i.location)
					localisation=localisation.split('](')
					localisation[0]=localisation[0][1:]
					localisation[1]=localisation[1][:-1]
					localisation[0]=localisation[0].split(':')
					info=info_gene(id_human=j[0],id_species=j[1],start=localisation[0][0],end=localisation[0][1],strand=localisation[1])
					dico_info_gene[info.id_species]=info
	in_handle.close()
	return dico_info_gene
	
get_info_gene(test,in_file)

def cut_fasta_gene(dico_info_gene,fasta)
	list_seq_fasta=list()
	
	return list_seq_fasta



def calcul_GC(list_sequence_gene):
	taux_GC=list()
	for i in list_sequence:
		GC=GC(i)
		taux_GC.append(GC)
	taux_GCGene=sum(taux_GC)/len(list_sequence_gene)
	return taux_GCGene
