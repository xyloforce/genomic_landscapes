#!/bin/bash
## general command
# https://www.orthodb.org/CMD?ARG1="value"&ARG2="value&..."
# Query : 1756 (DMD gene ID)
# ncbi : 1 (its a ncbi gene id)
# level : 32524 (amniota taxid)
# https://www.orthodb.org/search?query=1756&ncbi=1&level=32524
# 35298at33208 (one cluster)
# https://www.orthodb.org/group?id=35298at33208 (get info on the cluster fonction ; useless ?)
# https://www.orthodb.org/orthologs?id=35298at33208 (get genes in the cluster)

genomeFile=$1 #"GCF_000001405.39_GRCh38.p13_genomic.gff"
geneList=$2 #geneList.json

if ! [ -d logs ]; then
  mkdir logs
fi

if ! [ -f $genomFile ]; then
		  #download and extract a genome file gff
		  wget "ftp://ftp.ncbi.nlm.nih.gov/genomes/all/annotation_releases/9606/109.20200815/GCF_000001405.39_GRCh38.p13/GCF_000001405.39_GRCh38.p13_genomic.gff.gz" &> logs/wget.log &
		  gunzip $genomeFile.gz &> logs/gzip.log &
fi

####
# traitement with python
####
if ! [ -f $geneList ]; then
  python3 get_gene_names.py $genomeFile $geneList > logs/get_gene_names.log &
fi


#check if data from orthodb is present
if ! [ -d orthodb_data ]; then
  mkdir orthodb_data
fi

if ! [ -f orthodb_data/odb10v1_OG2genes.tab ]; then
  file="odb10v1_OG2genes.tab" # OGs to genes correspondence from https://www.orthodb.org/?page=filelist
  wget https://v101.orthodb.org/download/$file.gz -O orthodb_data/$file.gz >> logs/wget.log &
  gunzip orthodb_data/$file.gz  >> logs/gzip.log &
fi

if ! [ -f orthodb_data/odb10v1_gene_xrefs.tab ]; then
  file="odb10v1_gene_xrefs.tab" # OGs to genes correspondence from https://www.orthodb.org/?page=filelist
  wget https://v101.orthodb.org/download/$file.gz -O orthodb_data/$file.gz >> logs/wget.log &
  gunzip orthodb_data/$file.gz >> logs/gzip.log &
fi

python3 get_orthologs.py $geneList &> logs/get_orthologs.log &


echo end script
