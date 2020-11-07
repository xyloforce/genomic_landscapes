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
import os
import utilities


PATH_DATASET = "./datasets"
PATH_TO_DATA_DL = "/tmp/genome/"  # don’t forget / at end
SUBTYPE_LIST = ["accession", "taxon", "gene-id", "symbol"]  # from NCBI documentation
VERBOSE = True  # simple verbose mode, recommandation to false


def summary(type, value, subtype=None):
    """
    Return dic from dataset command summary of NCBI.
    By default is summary of gene ID.

    command summary of NCBI is : « datasets summary [gene/genome] [subtype] [value] »
    type is gene or genome
    subtype is optionnel and from SUBTYPE_LIST
    """
    if type == "gene" or type == "genome":
        if subtype is None:
            command = ' '.join((PATH_DATASET, "summary", type, "gene-id", str(value)))
        elif subtype in SUBTYPE_LIST:
            command = ' '.join((PATH_DATASET, "summary", type, subtype, str(value)))
        else:
            print(f"subtype {subtype} incorrect")
            return None

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
    From taxid get genome file with gff and fna, extracts them and return filelist.

    taxid is a taxid NCBI exemple : human, 10116, "Mus Musculus"
    """
    query_dict = summary("genome", str(taxid), subtype="taxon")
    # get assembly_accession code of taxid from query_dict
    # TODO: prendre le référence sinon faudra choisir…
    accession = query_dict["assemblies"][0]["assembly"]["assembly_accession"]
    command = ' '.join((PATH_DATASET, "download genome --exclude-protein --exclude-rna accession", accession))
    print("download started for assembly " + accession)

    # execute command
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if VERBOSE:
        # print download progressing
        while True:
            output = process.stdout.readline()
            if process.poll() is not None:
                break
            if output:
                print(output.decode('utf-8').rstrip())
    output, error = process.communicate()
    if error is None:
        # if ok, we unzip the genome file
        downloaded_file = zipfile.ZipFile("ncbi_dataset.zip")
        extracted_file_list = list()  # contain path to files extracted
        for archive_file in downloaded_file.namelist():
            # get gff and fna files
            if archive_file.endswith((".gff", ".fna")):
                file_to_extract = archive_file.split('/')[-1]
                # checking path conditions
                if not os.path.exists(PATH_TO_DATA_DL):
                    print(f"[Info] {PATH_TO_DATA_DL} not existed, so will create")
                if os.path.isfile(PATH_TO_DATA_DL + archive_file):
                    print(f"[Warning] {PATH_TO_DATA_DL + archive_file} destination is a file and will rewrite")
                try:
                    downloaded_file.extract(archive_file, path=PATH_TO_DATA_DL)
                    extracted_file_list.append(PATH_TO_DATA_DL + archive_file)
                    print(f"{file_to_extract} extracted")
                except NotADirectoryError as e:
                    # print(f"Error with path destination ({str(e).split()[-1]})")
                    print(f"Error with path destination ({str(e)})")
        return extracted_file_list
    else:
        print(f"error in command line : {error}")


def taxonomy(taxid):
    """
    get info from corresponding database ncbi taxonomy
    return xml
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    xml = utilities.get_xml(base_url, {"db": "taxonomy", "id": taxid, "rettype": "xml", "retmode": "text"})
    return xml


def lineage(taxid):
    """
    get only lineage from global taxonomy record
    """
    xml = taxonomy(taxid)
    lineage = utilities.query_xpath("//Lineage")
    return lineage


#  test if datasets is installed
try:
    process = subprocess.Popen("./datasets version".split(), stdout=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = process.communicate()
    print(f"datasets is present and this version is {stdout.strip()}")
except FileNotFoundError:
    print("You have to datasets install on your computer, you can try : « python3 -m pip install ncbi-datasets-pylib »\nOr you can download datasets programme from « https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/LATEST/linux-amd64/datasets »")
    sys.exit()

if __name__ == '__main__':
    # print(summary("gene", 920835))
    get_genome(2697049)
    pass
