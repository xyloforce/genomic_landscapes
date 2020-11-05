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
gene_count = 0
countPrint = 5000  # print at all number genes

for line in open(genomefile).readlines():
    if not line[0] == "#":
        columns = line.split("\t")
        if columns[2] == "gene":
            for value in re.findall("Dbxref=GeneID:(\d*)", columns[8]):
                gene_set.add(value)
                gene_count += 1
                with open(geneList, 'w') as json_file:
                    json.dump(list(gene_set), json_file)
                if gene_count % countPrint == 0:
                    print(f"extracting in progress… {gene_count} genes extracted")
print(f"extracting finished {gene_count} genes extracted")
