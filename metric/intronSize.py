#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################
# Library python for project M1 2020
# version 0.2
# datasets version use is 10.5
##########################################################

import sys
import re
import os
import json

VERBEUX = False


def get_gene_ID(csvFile, taxid):
    """
    Get gene Id from a csv result file.

    IN: a csv file and int(taxid)
    OUT: list of geneID
    """
    geneID = []
    with open(csvFile, 'r') as file:
        for line in file:
            row = line.split(',')
            if row[0] == str(taxid):
                geneID.append(int(row[2].strip()))
    print(f"{len(geneID)} genes found for taxid {taxid}")
    return geneID


def parsingGFF(geneIDlist, fileGFF, taxid):
    """
    Get start and stop exon from GFF file.

    IN: GFF and a gene ID list
    OUT: dict[geneID] = [(exon start, exon stop)…]
    """
    def inGene(geneID, limitDown, limitUp):
        if limitDown >= limitsGenes[geneID][0] and limitUp <= limitsGenes[geneID][1]:
            return True
        return False

    exons = {}
    limitsGenes = {}
    with open(fileGFF, 'r') as file:
        regex = "(exon|gene).(\d+).(\d+).+GeneID:(\d+)"
        # group :: 2 start ; 3 stop ; 4 GeneID
        for line in file:
            if line[0] == '#':
                continue
            match = re.search(regex, line)
            if match is None:
                continue
            if int(match.group(4)) in geneID:
                # geneID found by get_orthologs
                if match.group(1) == "gene":
                    limitsGenes[match.group(4)] = (match.group(2), match.group(3))
                if match.group(1) == "exon":
                    try:
                        # test if exon in gene limit
                        if inGene(match.group(4), match.group(2), match.group(3)):
                            # recording exons
                            if match.group(4) not in exons:
                                exons[match.group(4)] = {}
                            # get numero of exon
                            exonID = re.search("ID=exon-.+-(\d+);", line)
                            if exonID is None:
                                print(f"No ID exon found for gene {match.group(4)}")
                                # delete exon
                                print("gene ID deleted : ", end="")
                                exons.pop(match.group(4))
                            exons[match.group(4)][int(exonID.group(1))] = (int(match.group(2)), int(match.group(3)))
                    except Exception as e:
                        print(e)
    # calculating introns size
    introns = {"taxid": taxid}
    count = 0
    for gene in exons:
        # calculating size RNA : stop last exon - start first exon + 1
        sizeRNA = abs(exons[gene][min(exons[gene])][1] - exons[gene][max(exons[gene])][0] + 1)  # abs for cause strand
        sizeExon = 0
        for numExon in exons[gene]:
            sizeExon += exons[gene][numExon][1] - exons[gene][numExon][0] + 1
        if sizeRNA - sizeExon < 0:
            count += 1
            continue
        else:
            introns[gene] = sizeRNA - sizeExon

    if VERBEUX:
        print("Statistic")
        print(f"{len(limitsGenes)} genes found from GFF")
        print(f"{len(exons)} exons total")
        print(f"{len(introns)} introns calculated")
        print(f"{count} introns exclude")
    return introns


if __name__ == '__main__':
    geneID = (get_gene_ID(sys.argv[1], sys.argv[2]))
    intronSizeCalculated = parsingGFF(geneID, sys.argv[3], sys.argv[2])
    if VERBEUX:
        count = 0
        for gene in intronSizeCalculated:
            if count <= 10:
                print(f"gene {gene} have introns size of {intronSizeCalculated[gene]}")
                count += 1
            else:
                break
    else:
        if not os.path.isdir("metric/export"):
            os.mkdir("metric/export")
        # creating of filename json
        if '/' in sys.argv[3]:
            buffer = sys.argv[3].split('/')[-1]
            filename = buffer.split('.')[0]
        else:
            filename = sys.argv[3].split('.')[0]
        f = open(f"metric/export/{filename}.json", 'w')
        f.write(json.dumps(intronSizeCalculated))  # no inmdent to minimize file size
        f.close()
