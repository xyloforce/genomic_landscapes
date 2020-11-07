class species:
    def __init__(self, taxid, species_name, lineage=None):
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
            self.genes[human_gene]=list()
        self.genes[human_gene].append(ortholog)
        
    def get_genes:
        return genes
    
    def get_gene(human_gene):
        return genes[human_gene]
    
    def get_lineage:
        return lineage

    def __repr__(self): # just to check that it works well
        return str(len(self.genes))
