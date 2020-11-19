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

### Récupération des gff et fasta

```bash
python src/ncbi.py exe [taxid]
```

Les sorties se trouvent par défaut dans le répertoire `/tmp/genome`. Cette destination est modifiable dans le script.

### Calcul des métriques

Les scripts de calculs sont dans le dossier `metric`.

#### Taille des introns

C’est le script `intronSize.py` qui s’en occupe et le script `exportCsv.py` se charge de la concaténation des résultats dans un csv nommé `alexandria.csv` en hommage à la grande bibliothèque d’Alexandrie.

```shell
python metric/intronSize.py [results.csv] [taxid number] [genomic.gff]
python metric/exportCsv.py
```

Les sorties se trouvent dans `metric/data` pour `intronSize.py` et le fichier `alexendria.csv` est le csv importable dans R pour la génération de la heatmap.
