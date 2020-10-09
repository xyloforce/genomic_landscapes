import requests
import json
import time


# ====== function to make a correct request ====== #
def get_data(baseURL, payload):
    retry = True
    while retry:  # RETRY UNTIL SUCCES U SONOFAGUN
        time.sleep(1)
        try:
            # request add to the baseURL the params passed as dict
            request = requests.get(baseURL, params=payload)
        except requests.ConnectionError:
            print("Error : connection error. Retrying...")
        else:
            retry = False
        print("Requested " + request.url)
        return request.json()["data"]


# ====== creates gene:(groups) for each gene in (genes) ====== #
def search(genes, ncbi=1, level=32523):
    groups = dict()
    for gene in genes:
        data = get_data("https://www.orthodb.org/search",
                        {'query': gene, 'ncbi': ncbi, 'level': level})
        groups[gene] = data
    return groups


# ====== creates gene:(geneIDs) for each group in gene:(groups) ====== #
def orthologs(groups):
    orthologs = dict()
    for gene in groups:
        for group in groups[gene]:
            data = get_data("https://www.orthodb.org/orthologs", {"id": group})
            for organism in data:  # data is a list of organism
                for genes in organism["genes"]:  # organism is a dic
                    # genes is a dic of dic of dic (urk)
                    orthologs[gene] = list(set(orthologs[gene]).add(genes["gene_id"]["param"]))
    return orthologs


# ====== creates gene:(ncbi_geneIDs) for each geneID in gene:(geneIDs) ====== #
def ogdetails(orthologs):
    ncbi_orthologs = dict()
    for gene in orthologs:
        for ortholog in orthologs["gene"]:
            data = get_data("https://www.orthodb.org/ogdetails", {"id": ortholog})
            if "xrefs" in data:  # xrefs contains crossrefs, not always present
                for dict in data["xrefs"]:  # xrefs is a list of dic
                    if dict["type"] == "GeneID" or dict["type"] == "NCBIgene":  # option 1 to save the geneID
                        ncbi_orthologs[gene] = list(set(ncbi_orthologs[gene]).add(dict["id"]))
    return ncbi_orthologs
