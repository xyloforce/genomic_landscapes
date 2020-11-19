#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################
# Library python for project M1 2020
# version 0.1
# datasets version use is 10.5
##########################################################
import os
import json

allGene = {}
taxidRef = "9606"  # Homo Sapiens


def getHumanGene(taxid):
    """
    Get human gene from result.csv.
    """
    fileCorrespondance = "results.csv"  # file with header taxid,humangene,ncbiID
    humanGene = {}
    with open(fileCorrespondance, 'r') as file:
        for line in file:
            row = line.split(',')
            if str(row[0]) == str(taxid):
                humanGene[int(row[1])] = str(row[2])
    return humanGene


# concatenation all json
for file in os.listdir("metric/export"):
    if file[0] == '_':
        continue
    if os.path.isdir(file):
        continue
    filename = file.split('.')
    if filename[-1] == 'json':
        print(file)
        f = open(f"metric/export/{file}", 'r')
        dictBuffer = json.load(f)
        f.close()
        for gene in dictBuffer:
            if gene == "taxid":
                taxid = dictBuffer[gene]
                allGene[taxid] = {}
                continue
            allGene[taxid][str(gene)] = str(dictBuffer[gene])


# write result in csv
f = open("metric/alexandria.csv", 'w')

# create a reference
if taxidRef in allGene:
    taxidRefGene = allGene[taxidRef]
else:
    raise "Taxid ref not found in all data"

# creating header
ncbiToHumanGene = getHumanGene(9606)
listHumanGene = sorted(ncbiToHumanGene.keys())
f.write("taxid")
for humanGene in listHumanGene:
    f.write(f",{humanGene}")
f.write('\n')

# write rest
for taxid in allGene:
    if taxid == taxidRef:
        continue
    row = str(taxid)
    # get dict to correspond ncbi gene to human gene
    humanGeneToNCBI = getHumanGene(taxid)
    # write value metric in order of human gene
    for humanGene in listHumanGene:
        if humanGene in humanGeneToNCBI:
            geneID = humanGeneToNCBI[humanGene].strip()
            try:
                row += ',' + str(allGene[taxid][geneID])
            except KeyError:
                # gene exist but we could’t calculate the value metric
                row += ',Na'
        else:
            row += ',Na'  # no value, Na for R language
    row += '\n'
    f.write(row)
f.close()
print("INFO : Alexandria was built…")
