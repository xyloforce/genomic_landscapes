import requests
import json
import time
import glob
import os.path

def get_data(baseURL, payload):
        retry=True
        while retry:
            time.sleep(1)
            try:
                request=requests.get(baseURL, params=payload)
            except ConnectionError:
                print("Error : connection error. Retrying...")
            else:
                retry=False
        return request

#treated=0

#with open('gene_set.json') as json_file:
        #gene_set=json.load(json_file)
    
#try:
    #with open('clusters.json') as json_file:
        #cluster_dict=json.load(json_file)
#except FileNotFoundError:
    #print("File not found : starting from scratch")
    #cluster_dict=dict()

#for gene in gene_set:
    #treated+=1
    #if not gene in cluster_dict.keys():
        #request=get_data("https://www.orthodb.org/search", {'query':gene,'ncbi':1,'level':32523})
        #if not request.json()["data"]==[]:
            #cluster_dict[gene]=request.json()["data"]
    #with open('clusters.json', 'w') as json_file:
        #json.dump(cluster_dict, json_file)
    #print("Gene n°" + str(treated) + "/" + str(len(gene_set)))

treated=0

with open('clusters.json') as json_file:
        cluster_dict=json.load(json_file)
try:
    with open('orthologs.json') as json_file:
        orthologs_dict=json.load(json_file)
except FileNotFoundError:
    print("File not found : starting from scratch")
    orthologs_dict=dict()

for key in cluster_dict: # dict gene:species
    treated+=1
    orthologs_dict[key]=set()
    for cluster in cluster_dict[key]:
        orthologs_dict[key]=set(orthologs_dict[key])
        if not cluster in orthologs_dict.keys():
            request=get_data("https://www.orthodb.org/orthologs", {'id':cluster})
            if not request.json()["data"]==[]:
                for organism in request.json()["data"]:
                    for genes in organism["genes"]:
                        orthologs_dict[key].add(genes["gene_id"]["param"])
        orthologs_dict[key]=list(orthologs_dict[key])
        with open('orthologs.json', 'w') as json_file:
            json.dump(orthologs_dict, json_file)
    print("Cluster n°" + str(treated))
