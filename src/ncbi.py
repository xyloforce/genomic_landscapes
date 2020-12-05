#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################
# Library python for project M1 2020
# version 0.6
# datasets version use is 10.5
##########################################################
import sys
import ftplib
import gzip
import re

try:
    from . import utilities
except ImportError:
    import utilities

PATH_DATASET = "./datasets"
SUBTYPE_LIST = ["accession", "taxon", "gene-id", "symbol"]  # from NCBI documentation
VERBOSE = True  # simple verbose mode, recommandation to false

esearch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
efetch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def summary_genes(values):
    count = 0
    max_query = 199
    result_dict = dict()
    while count < len(values):
        to_request = values[count:count+max_query]
        result_dict.update(get_summary(to_request, lineage=False))
        count += max_query
    return result_dict


def taxonomy(taxid):
    """
    Get info from corresponding database ncbi taxonomy.

    return xml
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    xml = utilities.get_xml(base_url, {"db": "taxonomy", "id": taxid, "rettype": "xml", "retmode": "text", "api_key": "5d036b2735d9eaf6fde16f4f437f1cf4fd09"})
    return xml


def lineage(taxid):
    """
    Get only lineage from global taxonomy record.

    """
    xml = taxonomy(taxid)
    lineage = utilities.query_xpath(xml, ".//Lineage")
    lineage = lineage[0].text
    lineage = lineage.split("; ")
    lineage = lineage[15:]  # since we look at tetrapoda level we don't need the 15 items at the beginning
    return lineage


def get_summary(geneIDs, lineage=False):
    efetch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    result_dic = dict()

    xml = utilities.get_xml(efetch, {"db": "gene", "id": ",".join(geneIDs), "retmode": "xml", "api_key": "5d036b2735d9eaf6fde16f4f437f1cf4fd09"}, True, 0.1)
    elements = utilities.query_xpath(xml, "./")
    for geneID, element in zip(geneIDs, elements):
        if utilities.query_xpath(element, ".//Gene-track_geneid") != []:  # if it's not an empty match
            species_name = utilities.query_xpath(element, ".//Org-ref_taxname")[0].text
            taxid = utilities.query_xpath(element, ".//Org-ref_db/Dbtag/Dbtag_tag/Object-id/Object-id_id")[0].text
            if lineage:
                lineage = utilities.query_xpath(element, ".//OrgName_lineage")[0].text
                result_dic[geneID] = [species_name, taxid, lineage]
            else:
                result_dic[geneID] = [species_name, taxid]
    return result_dic


def get_genome(species_name):
    # query_dict = summary("genome", str(taxid), subtype="taxon")
    filelist = list()

    # get assembly_accession code of taxid from query_dict
    # accession = query_dict["assemblies"][0]["assembly"]["assembly_accession"]

    # get genome accession for species
    xml = utilities.get_xml(esearch, {"db": "genome", "term": species_name, "retmax": "200", "api_key": "5d036b2735d9eaf6fde16f4f437f1cf4fd09"})
    results = utilities.query_xpath(xml, ".//IdList/Id")

    if len(results) == 0:
        raise ValueError("No results found for " + species_name)
    elif not len(results) == 1:
        print("Warning : more than one result. Will pick the first, but you may check on ncbi that it was correct. Species name was " + species_name + "and we got " + str(len(results)) + " results")

    xml = utilities.get_xml(efetch, {"db": "genome", "id": results[0].text, "rettype": "docsum", "api_key": "5d036b2735d9eaf6fde16f4f437f1cf4fd09"})
    results = utilities.query_xpath(xml, './/Item[@Name="Assembly_Accession"]')
    accession = results[0].text

    print(accession)

    # get ftp URL for accession
    xml = utilities.get_xml(esearch, {"db": "assembly", "term": accession, "retmax": "200", "api_key": "5d036b2735d9eaf6fde16f4f437f1cf4fd09"})
    results = utilities.query_xpath(xml, ".//IdList/Id")
    if len(results) == 0:
        raise ValueError("No results found for " + species_name)
    elif not len(results) == 1:
        print("Warning : more than one result. Will pick the first, but you may check on ncbi that it was correct. Accession was " + accession + " and we got " + str(len(results)) + " results")

    xml = utilities.get_xml(efetch, {"db": "assembly", "id": results[0].text, "rettype": "docsum", "api_key": "5d036b2735d9eaf6fde16f4f437f1cf4fd09"})
    results = utilities.query_xpath(xml, './/FtpPath_RefSeq')

    filelist = get_files_from_ftp(results[0].text)
    print(filelist)
    extracted = list()

    for filename in filelist:
        if re.search("GCF_\d+.\d+_[A-Za-z.0-9]+_genomic\.fna\.gz", filename) is not None or filename.endswith(".gff.gz"):  # only one element in theory
            request = utilities.get_request("https://" + "/".join(results[0].text.split("/")[2:]) + "/" + filename)
            filename_uncompressed = ".".join(filename.split(".")[:-1])
            uncompressed_handler = open(filename_uncompressed, "wb")
            uncompressed_handler.write(gzip.decompress(request.content))
            uncompressed_handler.close()
            extracted.append(filename_uncompressed)

    return extracted


def get_files_from_ftp(url_fasta):
    url_ftp = url_fasta.split("/")[2]
    ftp = ftplib.FTP(url_ftp)
    ftp.login()
    ftp.cwd("/".join(url_fasta.split("/")[3:]))
    filelist = ftp.nlst()
    return filelist


if __name__ == '__main__':
    """
    arguments are :
    1 : get geneID : print taxname and taxid of given gene
    2 : exe species name : dl genome (fna et gff)
    """
    if sys.argv[1] == "get":
        print(get_summary(sys.argv[2]))
    elif sys.argv[1] == "exe":
        files = get_genome(sys.argv[2])  # test possible with 920835 or 2697049
        print(f"your files are in {files}")
    else:
        print("First argument unvailable, please choice between get or exe")
