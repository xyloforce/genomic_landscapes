configfile: "config.yaml"

rule graphs:
    input:
        expand("{metrics}.png", metrics = lambda: config["metrics"].keys())

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
    conda:
        "envs/python.yaml"
    shell:
        "python3 get_orthologs.py {input} {params}"

rule filter_species:
    input:
        "species_taxid_geneID.json"
    output:
        "results.csv"
    conda:
        "envs/R.yaml"
    shell:
        "Rscript species_selection.R {input}" # needs refactoring TODO

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
        "{metrics}.csv", "taxo_reference.csv", "gene_infos.csv"
    output:
        "{metrics}.png"
    params:
        lambda wildcards: config["metrics"][{wildcards.metrics}]
    conda:
        "envs/R.yaml"
    shell:
        "Rscript heatmap.R {input} {output} {params}" # same shit TODO
