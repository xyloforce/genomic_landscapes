import json
import zipfile
import os


class species:
    def __init__(self, taxid, species_name = None, lineage=None):
        """
        creates a species identified by taxid and containing empty dictionnary of orthologs
        """
        self.genes = dict()
        self.taxid = taxid
        self.species = species_name
        self.lineage = lineage

    def add_gene(self, human_gene, ortholog):
        """
        add an entry in the dic with key "human gene ID" and value "ortholog gene ID"
        """
        if human_gene not in self.genes:
            self.genes[human_gene] = list()
        self.genes[human_gene].append(ortholog)
        
    def export_species(self, path="./"):
        genes_species = self.taxid + "_genes.json"
        with open(genes_species, "w") as file_genes:
            json.dump(self.genes, file_genes)
        info_species = self.taxid + "_infos_species.txt"
        with open(info_species, "w") as file_infos:
            file_infos.write(self.species)
            file_infos.write(self.lineage)
        compressed = path + self.taxid + ".zip"
        with zipfile.ZipFile(compressed, "w") as file_archive:
            file_archive.write(genes_species)
            file_archive.write(info_species)
        os.remove(genes_species)
        os.remove(info_species)

    def set_lineage(self, lineage):
        self.lineage = lineage
        
    def set_genes(self, genes):
        self.genes = genes
    
    def set_name(self, name):
        self.species = name
    
    def get_genes(self):
        return self.genes
    
    def get_gene(self, human_gene):
        return self.genes[human_gene]
    
    def get_lineage(self):
        return self.lineage
    
    def get_taxid(self):
        return self.taxid

    def __repr__(self): # just to check that it works well
        return str(len(self.genes))
    

def build_back_species(filename):
    taxid = filename.split(".")[0]
    species_restored = species(taxid)
    with zipfile.ZipFile(filename) as archive:
        archive.extractall(".")
    genes_species = taxid + "_genes.json"
    with open(genes_species, "w") as file_genes:
        species_restored.set_genes(json.load(file_genes))
    info_species = taxid + "_infos_species.txt"
    with open(info_species, "w") as file_infos:
        species_restored.set_name(file_infos.readline().rstrip())
        species_restored.set_lineage(file_infos.readline().rstrip().split(";"))
    os.remove(genes_species)
    os.remove(info_species)
    return species_restored
