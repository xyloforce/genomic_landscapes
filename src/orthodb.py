#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################
# Library python for project M1 2020
# version 0.2
##########################################################
import requests
import json
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


def orthologs(groups):
    """
    creates gene:(geneIDs) for each group in gene:(groups)
    """
    orthologs = dict()
    for gene in groups:
        for group in groups[gene]:
            data = get_data("https://www.orthodb.org/orthologs", {"id": group})
            for organism in data:  # data is a list of organism
                for genes in organism["genes"]:  # organism is a dic
                    # genes is a dic of dic of dic (urk)
                    if gene not in orthologs:  # forgot to initialize
                        orthologs[gene] = list()
                    orthologs[gene].append(genes["gene_id"]["param"])
                    orthologs[gene] = list(set(orthologs[gene]))
    return orthologs


def ogdetails(orthologs):
    """
    creates gene:(ncbi_geneIDs) for each geneID in gene:(geneIDs)
    """
    ncbi_orthologs = dict()
    for gene in orthologs:
        for ortholog in orthologs[gene]:
            data = get_data("https://www.orthodb.org/ogdetails", {"id": ortholog})
            if "xrefs" in data:  # xrefs contains crossrefs, not always present
                for xref_dict in data["xrefs"]:  # xrefs is a list of dic
                    if xref_dict["type"] == "GeneID" or xref_dict["type"] == "NCBIgene":  # options to save the geneID
                        if gene not in ncbi_orthologs:  # forgot to initialize
                            ncbi_orthologs[gene] = list()
                        ncbi_orthologs[gene].append(xref_dict["id"])
                        ncbi_orthologs[gene] = list(set(ncbi_orthologs[gene]))
    return ncbi_orthologs
