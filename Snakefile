METRICS = ["GC3_exons", "GC_exons", "GC_flanking_before", "GC_flanking_after", "GC_gene", "intron_size"]
configfile: "config.yaml"

rule update:
    input:
        "results.csv"

rule graphs:
    input:
        expand("{metrics}.png", metrics = METRICS)

rule get_genes_names:
    input:
        config["human_annotation"]
    output:
        "gene_set.json"

rule get_orthologs:
    input:
        "gene_set.json"
    output:
        "species_taxid_geneID.json"

rule filter_species:
    input:
        "species_taxid_geneID.json"
    output:
        "results.csv"

rule metrics:
    input:
        "results.csv"
    output:
        "GC3_exons.csv", "GC_exons.csv", "GC_flanking_before.csv", "GC_flanking_after.csv", "GC_gene.csv", "intron_size.csv"

rule heatmap:
    input:
        "{metrics}.csv"
    output:
        "{metrics}.png"
