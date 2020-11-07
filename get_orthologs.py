import json
import time
import requests
import subprocess
import sys
import csv

import src.orthodb as orthodb
import src.ncbi as ncbi


PATH_TO_OG2genes = "orthodb_data/odb10v1_OG2genes.tab" # orthodb_data/odb10v1_OG2genes.tab
PATH_TO_GENE_XREFS = "orthodb_data/odb10v1_gene_xrefs.tab"  # orthodb_data/odb10v1_gene_xrefs.tab

def isNeeded(old_dic, saved_json):
    """
    check if an existing file is complete
    """
    try:
        with open(saved_json) as json_file:
            new_dic = json.load(json_file)
    except:
        return True
    else:
        needed = False
        for key in old_dic:
            if not len(old_dic[key]) == 0:
                if key not in new_dic:
                    needed = True
                    print("Missing value : " + key)
        return needed


def isNeeded2(old_list, saved_json):
    try:
        with open(saved_json) as json_file:
            new_dic = json.load(json_file)
    except:
        return True
    else:
        needed = False
        for value in old_list:
            if value not in new_dic:
                needed = True
                print("Missing value : " + value)
        return needed


# ====== load gene set generated from the other script ====== #
with open(sys.argv[1]) as json_file:
    genomeGenesList = json.load(json_file)

# ====== get the orthologs groups ====== #
if isNeeded2(genomeGenesList, 'orthologs_groups.json'):
    print("Searching orthologs")
    # Request NCBI and create a dict of human_gene:groups
    orthologs_groups = orthodb.search(genomeGenesList)
    with open('orthologs_groups.json', 'w') as json_file:
        json.dump(orthologs_groups, json_file)
else:
    with open('orthologs_groups.json') as json_file:
        orthologs_groups = json.load(json_file)

if isNeeded(orthologs_groups, 'gene_ids.json'):
    # ====== get the orthologs IDs ====== #
    print("Searching contents of orthologs groups")
    gene_ids = orthodb.orthologs(orthologs_groups, PATH_TO_OG2genes)  # gene_ids is dict of human:(orthodb_geneids)
    with open('gene_ids.json', 'w') as json_file:
        json.dump(gene_ids, json_file)
else:
    with open('gene_ids.json') as json_file:
        gene_ids = json.load(json_file)

if isNeeded(gene_ids, 'ncbi_gene_ids.json'):
    # ====== get the orthologs NCBI IDs ====== #
    print("Searching contents of orthologs groups")
    ncbi_gene_ids = orthodb.ogdetails(gene_ids, PATH_TO_GENE_XREFS)  # ncbi gene_ids is dict of human:(ncbi_geneids)
    with open('ncbi_gene_ids.json', 'w') as json_file:
        json.dump(ncbi_gene_ids, json_file)
else:
    with open('ncbi_gene_ids.json') as json_file:
        gene_ids = json.load(json_file)

csv_file = open("species_gene_humanortho.csv", "w", newline="")
fieldnames = ["human_gene", "species", "taxid", "geneID"]
writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
writer.writeheader()

for gene in ncbi_gene_ids:
    query_dict = ncbi.summary(" gene gene-id ", " ".join(ncbi_gene_ids[gene]))
    for ortholog in query_dict["genes"]:
        writer.writerow({"human_gene": gene,
                         "species": ortholog["gene"]["taxname"],
                         "taxid": ortholog["gene"]["tax_id"],
                         "geneID": ortholog["gene"]["gene_id"]})
