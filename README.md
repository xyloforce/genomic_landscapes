# Characterization of genomic landscapes

## Introduction

### Authors

This is a master's degree project for the LBBE (Laboratoire de Biométrique et de Biologie Évolutive), made by students from the *Master de bioinformatique* from Lyon.

### Context

The aim of this collection of scripts is to allow the user to plot various metrics relative to the genome's composition. It allows both to build a csv database of mappings between the genes of one species and all the other in the choosen group and to download and calculate metrics on the genome of selected species.

## How-to

### Installation

The wrapper script is written in Snakemake. Here's the procedure to follow to install snakemake through conda and allow for optimal integration :

1. Install [conda](https://docs.conda.io/en/latest/miniconda.html#linux-installers)
2. Setup bioconda channels:
```
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge
```
3. Install snakemake (`conda install snakemake`)

If you don't intend to use snakemake, you can install manually the dependencies and use the scripts one by one. You'll need the following python packages:

- `requests`
- `biopython`
- `bcbiogff`

and the R package `dplyr`.

You'll also need:

- any annotation file for the reference species (whose genes will be searched on orthodb)
- two files from orthodb: `OGs to genes correspondence` and `xrefs associated with Ortho DB gene` from https://www.orthodb.org/?page=filelist

File paths are to be set in the config.yaml or given to the proper script.

### Use

#### Conda

A global interface is available through snakemake. To use the full pipeline (creation of datasets, download of genome and plotting), run `snakemake -j [threads to use] --use-conda`. This will create the conda envs for the pipeline and then run it with the number of cores you specified (only requests to the NCBI are multi-threaded through the threading python lib, don't hesitate to specify a high number like 10 or 20).

To use only the update part, run `snakemake -j [threads to use] --use-conda update`.

To use only the plotting part, just make sure that all files created by update are in the folder and run `snakemake -j [threads to use] --use-conda` again.

#### Manual

Individual scripts do the following:

- `get_gene_names.py`: get gene names from gff, outputs a json file containing a list of genes and a csv containing informations about genes for plotting (chromosome, start position, symbol)
- `get_orthologs.py`: get the orthologs of geneIDs passed as json to the script, outputs two csv, one with taxonomy information and the other with the genes/species associated with each gene from the species
- `species_selection.R`: select species from the file created by the preceding script in order to optimize plotting
- `get_metrics_from_geneID.py`: download genomes and creates metrics files.
- `heatmap.R`: plot values created by the preceding script as an heatmap.
