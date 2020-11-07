# Caractérisation spatio-temporelle de l’évolution des paysages génomiques chez les vertébrés

## Introduction

### Auteurs

Ce projet universitaire a été confié à trois étudiants du master de bioinformatique de Lyon 1.

### Contexte

Représentation graphique de différentes métriques sur un génome de référence.

## Utilisation

L’adresse web vers le ficthier compressé du génome doit être modifiée dans `script.sh`.

Commandes à lancer :
```bash
./script.sh genomefile geneList
# genome is a gff file if not preset script will download a gff from ncbi
# geneList is a json file, contain list of gene extracted from genomeFile
```

Modification possible à faire dans le script :

- url du génome (ftp://ftp.ncbi.nlm.nih.gov/genomes/all/annotation_releases/9606/109.20200815/GCF_000001405.39_GRCh38.p13/GCF_000001405.39_GRCh38.p13_genomic.gff.gz)
- version des database d’orthodb (`OGs to genes correspondence` and `xrefs associated with Ortho DB gene` from https://www.orthodb.org/?page=filelist)
