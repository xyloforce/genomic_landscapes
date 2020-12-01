import json
import xml.etree.ElementTree
import requests
import time
import zipfile
import os

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


def get_xml(baseURL, payload={}):
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

def fuse_fasta(fasta_list, merged = "merged.fasta"):
    print("file will be created : " + merged)
    merged_file = open(merged, "w")
    for fasta_filename in fasta_list:
        if fasta_filename.endswith(".fna"):
            fasta_file = open(fasta_filename)
            for line in fasta_file:
                merged_file.write(line)
            fasta_file.close()
            os.remove(fasta_filename)
    return merged
