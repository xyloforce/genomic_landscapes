#!/usr/bin/env python3
# expect as input :
#1 json file from gene_names
#2 path to OG2 genes
#3 path to gene xrefs (see https://www.orthodb.org/?page=filelist)
#4 is the ID given below an NCBI taxid ?
#5 taxid or value to search in orthodb ; example: 32523, tetrapods

import json
import subprocess
import sys
import csv
import os

import src.orthodb as orthodb
import src.ncbi as ncbi
import src.utilities as utilities

PATH_TO_OG2genes = sys.argv[2] # orthodb_data/odb10v1_OG2genes.tab
PATH_TO_GENE_XREFS = sys.argv[3]  # orthodb_data/odb10v1_gene_xrefs.tab

# ====== load gene set generated from the other script ====== #
with open(sys.argv[1]) as json_file:
    genomeGenesList = json.load(json_file)

# ====== get the orthologs groups ====== #
if utilities.isNeeded2(genomeGenesList, 'orthologs_groups.json'):
    print("Searching orthologs")
    # Request NCBI and create a dict of human_gene:groups
    orthologs_groups = orthodb.search(genomeGenesList, sys.argv[4], sys.argv[5])
    with open('orthologs_groups.json', 'w') as json_file:
        json.dump(orthologs_groups, json_file)
else:
    with open('orthologs_groups.json') as json_file:
        orthologs_groups = json.load(json_file)
        print("Orthologs groups OK")

if utilities.isNeeded(orthologs_groups, 'gene_ids.json'):
    # ====== get the orthologs IDs ====== #
    print("Searching contents of orthologs groups")
    gene_ids = orthodb.orthologs(orthologs_groups, PATH_TO_OG2genes)  # gene_ids is dict of human:(orthodb_geneids)
    with open('gene_ids.json', 'w') as json_file:
        json.dump(gene_ids, json_file)
else:
    with open('gene_ids.json') as json_file:
        gene_ids = json.load(json_file)
        print("Orthologs IDs OK")
        del(orthologs_groups)

if utilities.isNeeded(gene_ids, 'ncbi_gene_ids.json'):
    # ====== get the orthologs NCBI IDs ====== #
    print("Searching NCBI IDs")
    ncbi_gene_ids = orthodb.ogdetails(gene_ids, PATH_TO_GENE_XREFS)  # ncbi gene_ids is dict of human:(ncbi_geneids)
    with open('ncbi_gene_ids.json', 'w') as json_file:
        json.dump(ncbi_gene_ids, json_file)
else:
    with open('ncbi_gene_ids.json') as json_file:
        ncbi_gene_ids = json.load(json_file)
        print("NCBI gene IDs OK")
        del(gene_ids)

species = dict() # dict of species_name:row_to_write, avoid duplicating taxo info, can't write row immediately because we need to harmonize taxo length first
max_len = 0 # len of the max lineage

last_query = list()
ignore = list()
try:
    h_csv_results = open("species_taxid_geneID.csv")
except FileNotFoundError:
    print("No previous csv, creating")
    h_csv_results = open("species_taxid_geneID.csv", "w")
    results_writer = csv.writer(h_csv_results)
    results_writer.writerow(["human_gene", "species", "taxid", "geneID"])
else:
    results_reader = csv.DictReader(h_csv_results)
    for row in results_reader:
        last_query = row["human_gene"], row["geneID"]
        ignore.append(row["human_gene"])
        if row["taxid"] not in species:
            print("Getting taxonomy for species taxid " + str(row["taxid"]))
            lineage = ncbi.lineage(row["taxid"])
            list_infos = [row["species"], row["taxid"]]
            list_infos += lineage
            if len(list_infos) > max_len:
                max_len = len(list_infos)
            species[row["taxid"]] = list_infos

    h_csv_results.close()
    h_csv_results = open("species_taxid_geneID.csv", "a")
    results_writer = csv.writer(h_csv_results)

h_csv_taxo = open("taxo_reference.csv", "w")
taxo_writer = csv.writer(h_csv_taxo)

for gene in ncbi_gene_ids:
    if gene not in ignore:
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
    if gene == last_query[0]: # it's the last gene queryed
        print("Restarting")
        write = False
        query_dict = ncbi.summary_genes(ncbi_gene_ids[gene])
        for ortholog in query_dict:
            if ortholog == last_query[1]:
                write = True
            if write:
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
    while len(species[taxid]) < max_len: # add empty columns until its OK
        species[taxid].append("")
    taxo_writer.writerow(species[taxid]) # then write row
