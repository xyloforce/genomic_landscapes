import json
import subprocess
import sys
import csv
import os

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
        print("Orthologs OK")

if isNeeded(orthologs_groups, 'gene_ids.json'):
    # ====== get the orthologs IDs ====== #
    print("Searching contents of orthologs groups")
    gene_ids = orthodb.orthologs(orthologs_groups, PATH_TO_OG2genes)  # gene_ids is dict of human:(orthodb_geneids)
    with open('gene_ids.json', 'w') as json_file:
        json.dump(gene_ids, json_file)
else:
    with open('gene_ids.json') as json_file:
        gene_ids = json.load(json_file)
        print("Orthologs groups OK")

if isNeeded(gene_ids, 'ncbi_gene_ids.json'):
    # ====== get the orthologs NCBI IDs ====== #
    print("Searching NCBI IDs")
    ncbi_gene_ids = orthodb.ogdetails(gene_ids, PATH_TO_GENE_XREFS)  # ncbi gene_ids is dict of human:(ncbi_geneids)
    with open('ncbi_gene_ids.json', 'w') as json_file:
        json.dump(ncbi_gene_ids, json_file)
else:
    with open('ncbi_gene_ids.json') as json_file:
        ncbi_gene_ids = json.load(json_file)
        print("NCBI gene IDs OK")

species = dict() # dict of species_name:row_to_write, avoid duplicating taxo info, can't write row immediately because we need to harmonize taxo length first
max_len = 0 # len of the max lineage

h_csv_results = open("species_taxid_geneID.csv", "w")
h_csv_taxo = open("taxo_reference.csv", "w")

results_writer = csv.writer(h_csv_results)
results_writer.writerow(["human_gene", "species", "taxid", "geneID"])
taxo_writer = csv.writer(h_csv_taxo)

for gene in ncbi_gene_ids:
    print("Querying gene " + str(list(ncbi_gene_ids.keys()).index(gene)) + "/" + str(len(ncbi_gene_ids.keys())))
    query_dict = ncbi.summary_genes(ncbi_gene_ids[gene])
    for ortholog in query_dict:
        species_name = query_dict[ortholog][0]
        taxid = query_dict[ortholog][1]
        results_writer.writerow([gene, species_name, taxid, ortholog])
        if taxid not in species:
            lineage = ncbi.lineage(taxid)
            list_infos = [species_name, taxid]
            list_infos += lineage
            if len(list_infos) > max_len:
                max_len = len(list_infos)
            species[taxid] = list_infos

for taxid in species:
    while len(species[taxid]) < max_length: # add empty columns until its OK
        species[taxid].append("")
    csv_taxonomy_writer.writerow(species[taxid]) # then write row

## OLD : species object
# species_dict = dict()

# for gene in ncbi_gene_ids:
#     query_dict = ncbi.summary_genes(' '.join(ncbi_gene_ids[gene]))
#     for ortholog in query_dict["genes"]:
#         taxid = ortholog["gene"]["tax_id"]
#         if taxid not in species_dict:
#             lineage = ncbi.lineage(taxid)
#             species_dict[taxid] = classSpecies.species(taxid, ortholog["gene"]["taxname"], lineage)
#         species_dict[taxid].add_gene(gene, ortholog["gene"]["gene_id"])

# for species in species_dict:
#     species.set_lineage(lineage(species.get_taxid()))

# for species in species_dict:
#     if not os.path.isdir("species"):
#         os.mkdir("species")
#     species_dict[species].export_species("species/")
