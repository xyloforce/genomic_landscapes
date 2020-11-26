import re
import json
import sys
import csv

gene_set = set()

#import genome file name
if len(sys.argv) == 3:
    genomefile = sys.argv[1] #file gff here
    geneList = sys.argv[2] #file json here
elif len(sys.argv) == 2:
    genomefile = sys.argv[1] #file gff here
    geneList = "gene_set.json" #file json here
else:
    print("No filename, exit")
    sys.exit()

#extract GeneID
gene_count = 0
countPrint = 5000  # print at all number genes

csv_handler = open("gene_infos.csv", "w")
csv_writer = csv.writer(csv_handler, dialect='excel')

for line in open(genomefile).readlines():
    if not line[0] == "#":
        columns = line.split("\t")
        if columns[2] == "gene":
            for value in re.findall("ID=gene-(\w*);Dbxref=GeneID:(\d*)", columns[8]):
                gene_set.add(value[1]) # match 2 : geneID
                csv_writer.writerow([value[1], value[0], columns[0][8:9]]) # geneID : symbol : chr
                gene_count += 1
                if gene_count % countPrint == 0:
                    print(f"extracting in progress… {gene_count} genes extracted")

with open(geneList, 'w') as json_file:
    json.dump(list(gene_set), json_file)
print(f"extracting finished {gene_count} genes extracted")
