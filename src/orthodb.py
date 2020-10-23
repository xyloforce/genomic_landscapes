#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################
# Library python for project M1 2020
# version 0.2
##########################################################
import requests
import json
import csv
import time
import simplejson


def get_data(baseURL, payload):
    """
    function to make a correct request
    """
    retry = True
    while retry:  # RETRY UNTIL SUCCES U SONOFAGUN
        time.sleep(1)
        try:
            # request add to the baseURL the params passed as dict
            request = requests.get(baseURL, params=payload)
            data = request.json()["data"]
        except (requests.ConnectionError, requests.HTTPError, requests.Timeout):
            print("Error : connection failed. Retrying...")
        except (ValueError, simplejson.errors.JSONDecodeError):
            print("Error : JSON invalid. Retrying...")
        else:
            retry = False
    print("Requested " + request.url)
    return data


def search(genes, ncbi=1, level=32523):
    """
    creates gene:(groups) for each gene in (genes)
    """
    groups = dict()
    for gene in genes:
        data = get_data("https://www.orthodb.org/search",
                        {'query': gene, 'ncbi': ncbi, 'level': level})
        groups[gene] = data
    return groups


def orthologs(groups, csv_source):
    """
    creates gene:(geneIDs) for each group in gene:(groups)
    """
    orthologs = dict()
    parsed = dict()
    csvfile = open(csv_source)
    csv_reader = csv.DictReader(csvfile, dialect=csv.excel_tab(), fieldnames=['OG', 'geneID'])
    for row in csv_reader:
        if row['OG'] not in parsed:
            parsed[row["OG"]] = list()
        parsed[row["OG"]].append(row["geneID"])
    for gene in groups:
        for group in groups[gene]:
            if gene not in orthologs:  # forgot to initialize
                orthologs[gene] = list()
            orthologs[gene] = orthologs[gene] + parsed[group]
            orthologs[gene] = list(set(orthologs[gene]))
    return orthologs


def ogdetails(gene_ids, csv_source):
    """
    creates gene:(ncbi_geneIDs) for each geneID in gene:(geneIDs)
    """
    with open(csv_source) as csvfile:
        convert = dict()
        csv_reader = csv.DictReader(csvfile, dialect=csv.excel_tab(), fieldnames=['ortho_id', 'value', 'type'])
        for row in csv_reader:
            if(row['type'] == "NCBIgid"):
                convert[row["ortho_id"]] = row["value"]
        ncbi_gene_ids = dict()
        for gene in gene_ids:
            if gene not in ncbi_gene_ids:  # forgot to initialize
                ncbi_gene_ids[gene] = list()
            for ortholog in gene_ids[gene]:
                if ortholog in convert:
                    ncbi_gene_ids[gene].append(convert[ortholog])
                    print("Parsed gene ID " + ortholog)
    return ncbi_gene_ids
