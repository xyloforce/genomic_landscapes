import sys
import json

def get_genome_from_ncbi(taxid):
    query_dict = summary("genome taxon ", taxid)
    accession = query_dict[
    command = "./datasets download genome --exclude-protein --exclude-rna " + taxid
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, universal_newlines=True)
    output, error = process.communicate()
    
def summary(type, gene_ids): # split : create a summary method returning the true summary already parsed
    command = "./datasets summary " + type + gene_ids
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, universal_newlines=True)
    output, error = process.communicate()
    try:
        query_dict = json.loads(output)
    except:
        print("error intercepted")
    return query_dict
