from cyvcf2 import VCF, Writer

# Filtering criteria
TARGET_GENES = {"BRCA1", "BRCA2", "TP53"}
IMPACT_LEVELS = {"MODERATE", "HIGH"}  # Keep only meaningful effects

vcf_path = "../data/annotated.vcf"
output_path = "../results/filtered_variants.vcf"

vcf = VCF(vcf_path)
out = Writer(output_path, vcf)

kept = 0
total = 0

for variant in vcf:
    total += 1
    anns = variant.INFO.get('ANN')
    if not anns:
        continue

    ann_entries = anns.split(",")
    for ann in ann_entries:
        fields = ann.split('|')
        if len(fields) < 4:
            continue
        impact = fields[2].strip()
        gene = fields[3].strip()

        if impact in IMPACT_LEVELS and gene in TARGET_GENES:
            out.write_record(variant)
            kept += 1
            break  # only need to match once

out.close()
vcf.close()

print(f"Total variants processed: {total}")
print(f"Variants passing filters: {kept}")
