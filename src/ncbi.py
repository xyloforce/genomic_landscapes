#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################
# Library python for project M1 2020
# version 0.1
# datasets version use is 10.5
##########################################################
import sys
import subprocess
import json
import zipfile


PATH_DATASET = "./datasets"
PATH_TO_DATA_DL = "/tmp/data"


def summary(type, gene_id):
    """
    Return dic of summary for given gene_id NCBI.

    command summary of NCBI is : « datasets summary [gene/genome] »
    type is gene or genome
    """
    if type == "gene" or type == "genome":
        command = "./datasets summary " + type + " gene-id " + str(gene_id)
        #  execute command
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, universal_newlines=True)
        output, error = process.communicate()
        if error is None:
            try:
                query_dict = json.loads(output)
                return query_dict
            except Exception as e:
                print(f"error catch {e}")
                return None
        else:
            print(f"Error in CLI : {error}")
            return None
    else:
        print(f"error in command type of 'datasets summary type', type must are « gene » or « genome » not {type}")



def get_genome(taxid):
    """
    from taxid get genome file with gff and fna, extracts them to /tmp and return filelist
    """
    query_dict = summary("genome taxon ", str(taxid))
    print(query_dict)
    accession = query_dict["assemblies"][0]["assembly"]["assembly_accession"]
    command = "./datasets download genome --exclude-protein --exclude-rna accession " + accession
    print("download started for assembly " + accession)
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, universal_newlines=True)
    output, error = process.communicate()
    downloaded_file = zipfile.ZipFile("ncbi_dataset.zip")
    extracted_file = list()
    file_list = downloaded_file.namelist()
    for archive_file in file_list:
        if archive_file[-3:] == "gff" or archive_file[-3:] == "fna":
            downloaded_file.extract(archive_file, path="/tmp")
            extracted_file.append(archive_file)
    return extracted_file




#  test if datasets is installed
try:
    process = subprocess.Popen("./datasets version".split(), stdout=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = process.communicate()
    print(f"datasets is present and this version is {stdout.strip()}")
except FileNotFoundError as e:
    print("You have to datasets install on your computer, you can try : « python3 -m pip install ncbi-datasets-pylib »\nOr you can download datasets programme from « https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/LATEST/linux-amd64/datasets »")
    sys.exit()

if __name__ == '__main__':
    print(summary("gene", 920835))
    pass
