#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##########################################################
# Library python for project M1 2020
# version 0.1
# datasets version use is 10.5
##########################################################

import sys
import re


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


def parsingGFF(geneIDlist, fileGFF):
    """
    Get start and stop exon from GFF file.

    IN: GFF and a gene ID list
    OUT: dict[geneID] = [(exon start, exon stop)…]
    """
    def inGene(geneID, limitDown, limitUp):
        if limitDown >= limitsGenes[geneID][0] and limitUp <= limitsGenes[geneID][1]:
            return True
        return False

    introns = {}
    exons = {}
    limitsGenes = {}
    with open(fileGFF, 'r') as file:
        regex = "(exon|gene).(\d).(\d).+GeneID:(\d+)"
        for line in file:
            match = re.search(regex, line)
            if match is None:
                continue
            if int(match.group(4)) in geneID:
                # geneID found by get_orthologs
                if match.group(1) == "gene":
                    limitsGenes[match.group(4)] = (match.group(2), match.group(3))
                if match.group(1) == "exon":
                    try:
                        if inGene(match.group(4), match.group(2), match.group(3)):
                            # recording exons
                            if match.group(4) not in exons:
                                exons[match.group(4)] = []
                            # TODO: fin exon final - start exon 1 - Σ(exons)
                            exons[match.group(4)].append(int(match.group(3)) - int(match.group(2)) + 1)
                    except Exception as e:
                        print(e)
    # calculating introns size
    for gene in limitsGenes:
        sizeGene = int(limitsGenes[gene][0]) - int(limitsGenes[gene][1])
        sizeExon = 0
        try:
            for size in exons[gene]:
                sizeExon += size
            introns[gene] = sizeGene - sizeExon
        except KeyError:
            pass

    print("debug")
    print(len(limitsGenes))
    print(len(exons))
    print(len(introns))
    return introns


if __name__ == '__main__':
    geneID = (get_gene_ID(sys.argv[1], sys.argv[2]))
    intronSizeCalculated = parsingGFF(geneID, sys.argv[3])
    count = 0
    for gene in intronSizeCalculated:
        if count <= 5:
            print(f"gene {gene} have introns size of {intronSizeCalculated[gene]}")
            count += 1
        else:
            break
