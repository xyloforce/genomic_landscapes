import json
import xml.etree.ElementTree
import requests
import time
import zipfile
import os
from .. import ClassSpecies

# some functions who can't go anywhere else


def get_request(baseURL, payload):
    """
    function to make a correct request
    """
    retry = True
    while retry:  # RETRY UNTIL SUCCES U SONOFAGUN
        time.sleep(1)
        try:
            # request add to the baseURL the params passed as dict
            request = requests.get(baseURL, params=payload)
        except (requests.ConnectionError, requests.HTTPError, requests.Timeout):
            print("Error : connection failed. Retrying...")
        else:
            retry = False
    print("Requested " + request.url)
    return request


def get_data(baseURL, payload):
    retry = True
    while retry:  # RETRY UNTIL SUCCES U SONOFAGUN
        try:
            request = get_request(baseURL, payload)
            data = request.json()["data"]
        except ValueError:
            print("Error : JSON invalid. Retrying...")
        else:
            retry = False
    return data


def get_xml(baseURL, payload):
    retry = True
    while retry:  # RETRY UNTIL SUCCES U SONOFAGUN
        try:
            request = get_request(baseURL, payload)
            data = xml.etree.ElementTree.fromstring(request.text)
        except ValueError:
            print("Error : XML invalid. Retrying...")
        else:
            retry = False
    return data


def query_xpath(xml, xpath):
    return xml.findall(xpath)


def build_back_species(filename):
    taxid = filename.split(".")[0]
    species_restored = ClassSpecies.species(taxid)
    with zipfile.ZipFile(filename) as archive:
        archive.extractall(".")
    genes_species = taxid + "_genes.json"
    with open(genes_species, "w") as file_genes:
        species_restored.set_genes(json.load(file_genes))
    info_species = taxid + "_infos_species.txt"
    with open(info_species, "w") as file_infos:
        species_restored.set_name(file_infos.readline().rstrip())
        species_restored.set_lineage(file_infos.readline().rstrip())
    os.remove(genes_species)
    os.remove(info_species)
    return species_restored
