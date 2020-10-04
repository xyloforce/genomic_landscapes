import re
import json

gene_set=set()

for line in open("GCF_000001405.39_GRCh38.p13_genomic.gff").readlines():
    if not line[0] == "#":
        columns=line.split("\t")
        if columns[2]=="gene":
            for value in re.findall("Dbxref=GeneID:(\d*)", columns[8]):
                gene_set.add(value)
                with open('gene_set.json', 'w') as json_file:
                    json.dump(list(gene_set), json_file)
