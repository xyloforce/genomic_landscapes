configfile: "config.yaml"

rule update:
    input:
        "results.csv"

rule graphs:
    input:
        expand("{metrics}.png", metrics = lambda: config["metrics"].keys())

rule get_genes_names:
    input:
        config["human_annotation"]
    output:
        "gene_set.json", "gene_infos.csv"
    shell:
        "python3 get_gene_names.py {input}"

rule get_orthologs:
    input:
        "gene_set.json"
    output:
        "species_taxid_geneID.json"
    shell:
        "python3 get_orthologs.py {input}"

rule filter_species:
    input:
        "species_taxid_geneID.json"
    output:
        "results.csv"
    shell:
        "Rscript species_selection.R {input}" # needs refactoring TODO

rule metrics:
    input:
        "results.csv"
    output:
        "GC3_exons.csv", "GC_exons.csv", "GC_flanking_before.csv", "GC_flanking_after.csv", "GC_gene.csv", "intron_size.csv"
    shell:
        "python3 get_metrics_from_geneID.py results.csv"

rule heatmap:
    input:
        "{metrics}.csv"
    output:
        "{metrics}.png"
    params:
        lambda wildcards: config["metrics"][{wildcards.metrics}]
    shell:
        "Rscript heatmap.R {input} {params}" # same shit TODO
