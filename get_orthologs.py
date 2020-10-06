import requests
import json
import time
import glob
import os.path
import xml.etree.ElementTree as xml

#====== function to make a correct request ======#
def get_data(baseURL, payload):
        retry=True
        while retry: # RETRY UNTIL SUCCES U SONOFAGUN
            time.sleep(1)
            try:
                request=requests.get(baseURL, params=payload) # request add to the baseURL the params passed as dict
            except ConnectionError:
                print("Error : connection error. Retrying...")
            else:
                retry=False
        return request

treated=0

#====== load saved objects ======#
with open('gene_set.json') as json_file: # if there is no file script need to crash
        gene_set=json.load(json_file) # gene set is created by the other script
    
try:
    with open('clusters.json') as json_file:
        cluster_dict=json.load(json_file)
except FileNotFoundError:
    print("File not found : starting from scratch")
    cluster_dict=dict()

#====== get dict of gene_id:list(orthologs_groups) ======#
for gene in gene_set:
    treated+=1
    if not gene in cluster_dict: # ensure that it is not in the (potentially) loaded dic
        request=get_data("https://www.orthodb.org/search", {'query':gene,'ncbi':1,'level':32523}) # params from the orthodb api, taxid is the bilateria one
        if not request.json()["data"]==[]:
            cluster_dict[gene]=request.json()["data"] # is a list of orthodb groups
    with open('clusters.json', 'w') as json_file:
        json.dump(cluster_dict, json_file)
    print("Gene n°" + str(treated) + "/" + str(len(gene_set)))

treated=0

with open('clusters.json') as json_file:
        cluster_dict=json.load(json_file)
try:
    with open('orthologs.json') as json_file:
        orthologs_dict=json.load(json_file)
except FileNotFoundError:
    print("File not found : starting from scratch")
    orthologs_dict=dict()
    
#====== get dict of gene_id:list(orthodb_geneid_from_groups) ======#
for key in cluster_dict: # dict gene:orthologs_groups
    treated+=1
    orthologs_dict[key]=set() # ensure that no geneid is here twice if groups overlaps
    for cluster in cluster_dict[key]:
        orthologs_dict[key]=set(orthologs_dict[key]) # transform it back into a set (see below)
        if not cluster in orthologs_dict: # ensure that it is not in the (potentially) loaded dic
            request=get_data("https://www.orthodb.org/orthologs", {'id':cluster}) # cluster is the group ID
            if not request.json()["data"]==[]:
                for organism in request.json()["data"]: # data is a list of organism
                    for genes in organism["genes"]: # organism is a dic
                        orthologs_dict[key].add(genes["gene_id"]["param"]) # genes is a dic of dic of dic (urk)
        orthologs_dict[key]=list(orthologs_dict[key]) # transform the set in a list bc json doesn't like sets
        with open('orthologs.json', 'w') as json_file:
            json.dump(orthologs_dict, json_file)
    print("Cluster n°" + str(treated))
    
with open('orthologs.json') as json_file:
        orthologs_dict=json.load(json_file)

try:
    with open('orthologs_ncbi.json') as json_file:
        orthologs_dict_ncbi=json.load(json_file)
except FileNotFoundError:
    print("File not found : starting from scratch")
    orthologs_dict_ncbi=dict()

#====== get dict of gene_id:list(ncbi_geneid_from_groups) ======#
for key in orthologs_dict:
    orthologs_dict_ncbi[key]=set()
    for gene_id in orthologs_dict[key]:
        orthologs_dict_ncbi[key]=set(orthologs_dict_ncbi[key])
        if not gene_id in orthologs_dict_ncbi:
            request=get_data("https://www.orthodb.org/ogdetails", {'id':gene_id}) # get details about the geneID
            if not request.json()["data"]==[]:
                if "xrefs" in request.json()["data"]: # xrefs contains crossrefs, not always present
                    for dict in request.json()["data"]["xrefs"]: # xrefs is a list of dic
                        if dict["type"]=="GeneID": # option 1 to save the geneID
                            orthologs_dict_ncbi[key].add(dict["id"])
                        elif dict["type"]=="NCBIgene": # option 2 to save the geneID
                            orthologs_dict_ncbi[key].add(dict["id"])
        orthologs_dict_ncbi[key]=list(orthologs_dict_ncbi[key])
        with open('orthologs_ncbi.json', 'w') as json_file:
            json.dump(orthologs_dict_ncbi, json_file)

with open('orthologs_ncbi.json') as json_file:
        orthologs_dict_ncbi=json.load(json_file)

try:
    with open('species.json') as json_file:
        species=json.load(json_file)
except FileNotFoundError:
    print("File not found : starting from scratch")
    species=dict()

#====== get dict of gene_id:list(ncbi_taxid) ======#
for key in orthologs_dict_ncbi:
    species[key]=set()
    for gene in orthologs_dict_ncbi[key]:
        orthologs_dict_ncbi[key]=set(orthologs_dict_ncbi[key])
        if not gene in species:
            request=get_data("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi", {'db':"gene", "id":gene})
            try:
                xml_file=xml.parse(request.text) # oh no its xml :(
            except:
                print("XML file invalid : " + gene) # dunno if it works so just in case save the gene for future reference
            else:
                if not xml_file.findall("//TaxID")[0].text == "":
                    species[key].add(xml_file.findall("//TaxID")[0].text) # get the freaking taxid
        orthologs_dict[key]=list(orthologs_dict[key]) 
        with open('orthologs_ncbi.json', 'w') as json_file:
            json.dump(orthologs_dict_ncbi, json_file)
