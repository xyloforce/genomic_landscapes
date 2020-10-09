import json
import time
import requests
import xml.etree.ElementTree as xml

import orthodb


# ====== function to make a request ====== #
def get_request(baseURL, payload):
    retry = True
    while retry:  # RETRY UNTIL SUCCES U SONOFAGUN
        time.sleep(1)
        try:
            request = requests.get(baseURL, params=payload)
        except requests.ConnectionError:
            print("Error : connection error. Retrying...")
        else:
            retry = False
        print("Requested " + request.url)
        return request


# ====== load gene set generated from the other script ====== #
with open('gene_set.json') as json_file:
    genes = json.load(json_file)

# ====== get the orthologs groups ====== #
print("Searching orthologs")
orthologs_groups = orthodb.search(genes)
with open('orthologs_groups.json', 'w') as json_file:
    json.dump(orthologs_groups, json_file)

# ====== get the orthologs IDs ====== #
print("Searching contents of orthologs groups")
gene_ids = orthodb.orthologs(orthologs_groups)
with open('gene_ids.json', 'w') as json_file:
    json.dump(gene_ids, json_file)

# ====== get the orthologs NCBI IDs ====== #
print("Searching ncbi IDs")
ncbi_gene_ids = orthodb.ogdetails(gene_ids)
with open('ncbi_gene_ids.json', 'w') as json_file:
    json.dump(ncbi_gene_ids, json_file)

print("Requesting the NCBI")
# ====== get dict of gene_id:list(ncbi_taxid) ====== #
species = dict()
for human_gene in ncbi_gene_ids:
    for ortholog in ncbi_gene_ids[human_gene]:
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        request = get_request(url, {'db': "gene", "id": ortholog})
        try:
            xml_file = xml.parse(request.text)  # oh no its xml :(
        except:
            print("XML file invalid : " + ortholog)  # just in case
        else:
            # get the freaking taxid
            if not xml_file.findall("//TaxID")[0].text == "":
                species[human_gene] = list(set(species[human_gene]).add(xml_file.findall("//TaxID")[0].text))

with open('species.json', 'w') as json_file:
    json.dump(species, json_file)
