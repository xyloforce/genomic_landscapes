configfile: "config.yaml"

rule graphs:
    input:
        expand("{metrics}.png", metrics = config["metrics"].keys())

rule update:
    input:
        "results.csv"

rule get_genes_names:
    input:
        config["annotation"]
    output:
        "gene_set.json", "gene_infos.csv"
    conda:
        "envs/python.yaml"
    shell:
        "python3 get_gene_names.py {input}"

rule get_orthologs:
    input:
        "gene_set.json"
    output:
        "species_taxid_geneID.json", "taxo_reference.csv"
    params:
        config["OG2_genes"], config["Genes_XRefs"], config["OrthoDBSearchID"], config["isPreviousNCBI"]
    threads:
        worflow.cores
    conda:
        "envs/python.yaml"
    shell:
        "python3 get_orthologs.py {input} {params} {threads}"

rule filter_species:
    input:
        "species_taxid_geneID.json", "taxo_reference.csv"
    output:
        "results.csv"
    params:
        config["keep_sample_duplicate"]
    conda:
        "envs/R.yaml"
    shell:
        "Rscript species_selection.R {input}"

rule metrics:
    input:
        "results.csv"
    output:
        "GC3_exons.csv", "GC_exons.csv", "GC_flanking_before.csv", "GC_flanking_after.csv", "GC_gene.csv", "intron_size.csv"
    conda:
        "envs/python.yaml"
    shell:
        "python3 get_metrics_from_geneID.py results.csv"

rule heatmap:
    input:
        "metrics_{metrics}.tsv", "taxo_reference.csv", "gene_infos.csv"
    output:
        "{metrics}.png"
    params:
        lambda wildcards: config["metrics"][wildcards.metrics]
    conda:
        "envs/R.yaml"
    shell:
        "Rscript heatmap.R {input} {output} {params}"
