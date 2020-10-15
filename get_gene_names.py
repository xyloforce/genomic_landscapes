import re
import json
import sys

gene_set = set()

#import genome file name
if len(sys.argv) == 3:
    genomefile = sys.argv[1] #file gff here
    geneList = sys.argv[2] #file json here
else:
    print("No filename, exit")
    sys.exit()

#extract GeneID
for line in open(genomefile).readlines():
    if not line[0] == "#":
        columns = line.split("\t")
        if columns[2] == "gene":
            for value in re.findall("Dbxref=GeneID:(\d*)", columns[8]):
                gene_set.add(value)
                with open(geneList, 'w') as json_file:
                    json.dump(list(gene_set), json_file)
