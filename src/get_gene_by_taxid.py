#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################
# Library python for project M1 2020
# version 0.1
##########################################################
import sys
import json

# Arguments
if not len(sys.argv) == 4:
    SPECIES_FILE_INPUT = "species.json" # default in get_orthologs.py
    ORTHOLOGS_FILE_INPUT = "orthologs_groups.json" # default in get_orthologs.py
    TAXID_SELECT = "9606" # Homo Sapiens
else:
    SPECIES_FILE_INPUT = sys.argv[1]
    ORTHOLOGS_FILE_INPUT = sys.argv[2]
    TAXID_SELECT = int(sys.argv[3])

# Variables
speciesDic_gene = json.load(open(SPECIES_FILE_INPUT, 'r'))
orthoDic_gene = json.load(open(ORTHOLOGS_FILE_INPUT, 'r'))
dataList_gene_export = [] # export [("id_humain_1","id_orth_espece"),("id_humain_2","id_orth_espece"),…]

# Script
for gene_id in speciesDic_gene:
    for taxid in speciesDic_gene[gene_id]:
        if taxid == TAXID_SELECT:
            # get gene ID of orthodb from orthologs_groups.json
            buffer = orthoDic_gene[gene_id][0] # default first element…
            gene_id_orthodb = buffer.split("at")[0]
            dataList_gene_export.append((gene_id, gene_id_orthodb))

# verbose
print(f"{len(dataList_gene_export)} gene exported")
print(dataList_gene_export)
"""
test=[("id_humain_1","id_orth_espece"),("id_humain_2","id_orth_espece"),("id_humain_3","id_orth_espece")]

Donc des tuple associant pour chaque gène humain son orthologue dans l'espèce en question en sachant qu'il n'y a qu'un seul orthologue
"""
