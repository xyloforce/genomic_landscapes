import json
import xml.etree.ElementTree
import requests
import time
import zipfile
import os

# some functions who can't go anywhere else

def isNeeded(old_dic, saved_json):
    """
    check if an existing file is complete
    """
    try:
        with open(saved_json) as json_file:
            new_dic = json.load(json_file)
    except:
        return True
    else:
        needed = False
        for key in old_dic:
            if not len(old_dic[key]) == 0:
                if key not in new_dic:
                    needed = True
                    print("Missing value : " + key)
        return needed


def isNeeded2(old_list, saved_json):
    try:
        with open(saved_json) as json_file:
            new_dic = json.load(json_file)
    except:
        return True
    else:
        needed = False
        for value in old_list:
            if value not in new_dic:
                needed = True
                print("Missing value : " + value)
        return needed

def get_request(baseURL, payload={}, verbose=False, wait=1):
    """
    Try to make a correct request.
    """
    retry = True
    numberTry = 0
    while retry and numberTry < 10:  # retry max 10
        time.sleep(wait + numberTry)
        # request add to the baseURL the params passed as dict
        request = requests.get(baseURL, params=payload)
        if verbose:
            print("Requested " + request.url, end=" - code: ")
        if request.status_code == 200:
            if verbose:
                print("200 OK")
            return request
        else:
            if request.status_code == 404:
                retry = False
                print("404 Not Found")
            elif str(request.status_code)[0] == "4":
                print(f"{request.status_code}\nClient Error. Retrying...")
                numberTry += 1
                print(f"Try n° {numberTry}")
            elif str(request.status_code)[0] == "5":
                print(f"{request.status_code}\nServer Error. Retrying...")
                time.sleep(3)
                numberTry += 1
                print(f"Try n° {numberTry}")
            else:
                print(f"{request.status_code}\nConnection failed. Retrying...")
                numberTry += 1
                print(f"Try n° {numberTry + 1}")
        # return request
    print(request.url)
    raise Exception("Bad connection to NCBI or Bad code, in any case check the code and the url request")
    return None  # no request body


def get_data(baseURL, payload={}, verbose = False, wait=1):
    retry = True
    while retry:  # RETRY UNTIL SUCCES U SONOFAGUN
        try:
            request = get_request(baseURL, payload, verbose, wait)
            data = request.json()["data"]
        except ValueError:
            print("Error : JSON invalid. Retrying...")
        else:
            retry = False
    return data


def get_xml(baseURL, payload={}, verbose = False, wait=1):
    retry = True
    while retry:  # RETRY UNTIL SUCCES U SONOFAGUN
        try:
            request = get_request(baseURL, payload, verbose, wait)
            data = xml.etree.ElementTree.fromstring(request.text)
        except ValueError:
            print("Error : XML invalid. Retrying...")
        else:
            retry = False
    return data


def query_xpath(xml, xpath):
    return xml.findall(xpath)


def fuse_fasta(fasta_list, merged="merged.fasta"):
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
