#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################
# Library python for project M1 2020
# version 0.1
##########################################################
import sys
import json


def exportGenesByTaxid(SPECIES_FILE_INPUT, ORTHOLOGS_FILE_INPUT, TAXID_SELECT=0):
    """
    extract gene by taxid from a json file
    IN : json file {"gene_id":[taxidlist]} ; json file {gene_id:[geneOrthoDB]} ; number taxid
    OUT : dict [taxid] = [("id_gene_1", "id_orth_espece"), ("id_gene_2", "id_orth_espece"), …]
    """
    # Variables
    speciesDic_gene = json.load(open(SPECIES_FILE_INPUT, 'r'))
    orthoDic_gene = json.load(open(ORTHOLOGS_FILE_INPUT, 'r'))
    gene_count = 0

    if TAXID_SELECT == 0:
        dataDic_gene_export = {}  # export [taxid]=[("id_gene_1","id_orth_espece"),("id_gene_2","id_orth_espece"),…]
    else:
        dataDic_gene_export = {TAXID_SELECT: []}

    # Script
    for gene_id in speciesDic_gene:
        for taxid in speciesDic_gene[gene_id]:
            # get gene ID of orthodb from orthologs_groups.json
            gene_id_orthodb = orthoDic_gene[gene_id][0].split("at")[0]  # default first element…
            if taxid == TAXID_SELECT:
                dataDic_gene_export[TAXID_SELECT].append((gene_id, gene_id_orthodb))
                gene_count += 1
            elif TAXID_SELECT == 0:
                if taxid not in dataDic_gene_export.keys():
                    dataDic_gene_export[taxid] = []
                dataDic_gene_export[taxid].append((gene_id, gene_id_orthodb))
                gene_count += 1
            else:
                continue

    # verbose
    print(f"{len(dataDic_gene_export)} taxid exported")
    print(f"{gene_count} gene exported")
    return(dataDic_gene_export)


if __name__ == '__main__':
    # Arguments
    if not len(sys.argv) == 4:
        SPECIES_FILE_INPUT = "species.json"  # default in get_orthologs.py
        ORTHOLOGS_FILE_INPUT = "orthologs_groups.json"  # default in get_orthologs.py
        TAXID_SELECT = 0  # default all taxid will select
    else:
        SPECIES_FILE_INPUT = sys.argv[1]
        ORTHOLOGS_FILE_INPUT = sys.argv[2]
        TAXID_SELECT = int(sys.argv[3])
        print(exportGenesByTaxid(SPECIES_FILE_INPUT, ORTHOLOGS_FILE_INPUT, TAXID_SELECT))
