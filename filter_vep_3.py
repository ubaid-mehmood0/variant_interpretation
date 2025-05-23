from cyvcf2 import VCF
from collections import Counter

vcf = VCF("../results/filtered_variants.vcf")

gene_counter = Counter()
impact_counter = Counter()
zygosity_counter = Counter()

for var in vcf:
    anns = var.INFO.get("ANN")
    if anns:
        for ann in anns.split(","):
            fields = ann.split("|")
            if len(fields) >= 4:
                impact = fields[2].strip()
                gene = fields[3].strip()
                gene_counter[gene] += 1
                impact_counter[impact] += 1
                break  # only need one annotation per variant

    # Zygosity from genotypes
    for sample_gt in var.genotypes:
        gt = sample_gt[:2]  # diploid, e.g., [0, 1] or [1, 1]
        if gt[0] != gt[1]:
            zygosity_counter["heterozygous"] += 1
        elif gt[0] == gt[1] and gt[0] != 0:
            zygosity_counter["homozygous_alt"] += 1
        else:
            zygosity_counter["homozygous_ref"] += 1

print("Variants per gene:", gene_counter)
print("Impact summary:", impact_counter)
print("Zygosity breakdown:", zygosity_counter)
