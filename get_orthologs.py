import json
import time
import requests
import sys

import src.orthodb as orthodb


def get_request(baseURL, payload):
    """
    function to make a request
    """
    retry = True
    while retry:  # RETRY UNTIL SUCCES U SONOFAGUN
        time.sleep(1)
        try:
            request = requests.get(baseURL, params=payload)
        except (requests.ConnectionError, requests.HTTPError, requests.Timeout):
            print("Error : connection failed. Retrying...")
        except ValueError:
            print("Error : JSON invalid. Retrying...")
        else:
            retry = False
    print("Requested " + request.url)
    return request


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
    # Request NCBI and create a dict
    orthologs_groups = orthodb.search(genomeGenesList)
    with open('orthologs_groups.json', 'w') as json_file:
        json.dump(orthologs_groups, json_file)
else:
    with open('orthologs_groups.json') as json_file:
        orthologs_groups = json.load(json_file)

if isNeeded(orthologs_groups, 'gene_ids.json'):
    # ====== get the orthologs IDs ====== #
    print("Searching contents of orthologs groups")
    gene_ids = orthodb.orthologs(orthologs_groups)  # gene_ids is dict
    with open('gene_ids.json', 'w') as json_file:
        json.dump(gene_ids, json_file)
else:
    with open('gene_ids.json') as json_file:
        gene_ids = json.load(json_file)

# ====== get the orthologs NCBI IDs ====== #
if isNeeded(gene_ids, 'ncbi_gene_ids.json'):
    print("Searching ncbi IDs")
    ncbi_gene_ids = orthodb.ogdetails(gene_ids)
    with open('ncbi_gene_ids.json', 'w') as json_file:
        json.dump(ncbi_gene_ids, json_file)
else:
    with open('ncbi_gene_ids.json') as json_file:
        ncbi_gene_ids = json.load(json_file)

print("Requesting the NCBI")
# ====== get dict of gene_id:list(ncbi_taxid) ====== #
species = dict()
for human_gene in ncbi_gene_ids:
    for geneID_ortholog in ncbi_gene_ids[human_gene]:
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        request = get_request(url, {'db': "gene", "id": geneID_ortholog, "format": "json"})
        if human_gene not in species:  # forgot to initialize
            species[human_gene] = list()
        species[human_gene].append(request.json()["result"][geneID_ortholog]["organism"]["taxid"])
        species[human_gene] = list(set(species[human_gene]))
with open('species.json', 'w') as json_file:
    json.dump(species, json_file)
