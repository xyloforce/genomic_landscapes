## general command
# https://www.orthodb.org/CMD?ARG1="value"&ARG2="value&..."
# Query : 1756 (DMD gene ID)
# ncbi : 1 (its a ncbi gene id)
# level : 32524 (amniota taxid)
# https://www.orthodb.org/search?query=1756&ncbi=1&level=32524
# 35298at33208 (one cluster)
# https://www.orthodb.org/group?id=35298at33208 (get info on the cluster fonction ; useless ?)
# https://www.orthodb.org/orthologs?id=35298at33208 (get genes in the cluster)

wget "ftp://ftp.ncbi.nlm.nih.gov/genomes/all/annotation_releases/9606/109.20200815/GCF_000001405.39_GRCh38.p13/GCF_000001405.39_GRCh38.p13_genomic.gff.gz" &> wget.log &
gunzip "GCF_000001405.39_GRCh38.p13_genomic.gff.gz" &> gzip.log &
python3 get_gene_names.py &> get_gene_names.log &
python3 get_orthologs.py &> get_orthologs.log &
