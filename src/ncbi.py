import sys
import subprocess
import json
import zipfile


def get_genome_from_ncbi(taxid):
    query_dict = summary("genome taxon ", taxid)
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


def summary(type, gene_ids): # split : create a summary method returning the true summary already parsed
    command = "./datasets summary " + type + gene_ids
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, universal_newlines=True)
    output, error = process.communicate()
    try:
        query_dict = json.loads(output)
    except:
        print("error intercepted")
    return query_dict
