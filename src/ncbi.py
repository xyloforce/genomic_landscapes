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
import time
from . import utilities

PATH_DATASET = "./datasets"
PATH_TO_DATA_DL = "/tmp/genome/"  # don’t forget / at end
SUBTYPE_LIST = ["accession", "taxon", "gene-id", "symbol"]  # from NCBI documentation
VERBOSE = True  # simple verbose mode, recommandation to false
# TODO: dataset path


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
            raise Exception("Wrong subtype provided")
    else:
        print(f"error in command type of 'datasets summary type', type must be « gene » or « genome » not {type}")
        raise Exception("Wrong type provided")
    retry = True
    try_count = 0
    #  execute command
    while retry:
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, universal_newlines=True)
        output, error = process.communicate()
        if error is None:
            try:
                query_dict = json.loads(output)
            except ValueError:
                print(command)
                if try_count < 10:
                    print("Value error catched, retrying in " + str(try_count) + " seconds")
                    time.sleep(1*try_count)
                    try_count += 1
                else:
                    raise ValueError("An unexpected error happened : please read the error message")
            except Exception as e:
                raise Exception("An unexpected error happened : please read the error message")
            else:
                retry = False
        else:
            print(f"Error in CLI : {error}")
            return None
    return query_dict


def summary_genes(values):
    values = values.split()
    count = 0
    repeat = True
    result_dict = {"genes": list()}
    while count < len(values):
        to_request = " ".join(values[count:count+15])
        print(to_request)
        try:
            middle_dict = summary("gene", to_request, "gene-id")
        except ValueError:
            middle_dict = {"genes": list()}
        result_dict["genes"].extend(middle_dict["genes"])
        count += 15
    return result_dict


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
                    os.mkdir(PATH_TO_DATA_DL)
                if os.path.isfile(PATH_TO_DATA_DL + archive_file):
                    print(f"[Warning] {PATH_TO_DATA_DL + archive_file} destination is a file and will rewrite")
                try:
                    # downloaded_file.extract(archive_file, path=PATH_TO_DATA_DL)
                    #extracted_file_list.append(PATH_TO_DATA_DL + archive_file)
                    extension = file_to_extract.split(".")[-1]
                    pathFile = PATH_TO_DATA_DL + accession + '.' + extension
                    with open(pathFile, 'wb') as f:
                        f.write(downloaded_file.read(archive_file))
                        extracted_file_list.append(pathFile)
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
    lineage = utilities.query_xpath(xml, ".//Lineage")
    lineage = lineage[0].text
    lineage = lineage.split("; ")
    lineage = lineage[15:] # since we look at tetrapoda level we don't need the 15 items at the beginning
    return lineage


#  test if datasets is installed
try:
    process = subprocess.Popen("./datasets version".split(), stdout=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = process.communicate()
    print(f"datasets is present and this version is {stdout.strip()}")
except FileNotFoundError:
    try:
        process = subprocess.Popen("datasets version".split(), stdout=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = process.communicate()
        print(f"datasets is present and this version is {stdout.strip()}")
    except FileNotFoundError:
        print("You have to install datasets on your computer, either try : « python3 -m pip install ncbi-datasets-pylib » or download datasets from « https://ftp.ncbi.nlm.nih.gov/pub/datasets/command-line/LATEST/linux-amd64/datasets »")
        sys.exit()

if __name__ == '__main__':
    """
    arguments are :
    1 : get or exe
    2 : taxid
    """
    if sys.argv[1] == "get":
        print(summary("genome", sys.argv[2], "taxon"))
    elif sys.argv[1] == "exe":
        files = get_genome(sys.argv[2])  # test possible with 920835 or 2697049
        print(f"your files are in {files}")
    else:
        print("First argument unvailable, please choice between get or exe")
