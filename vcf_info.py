from cyvcf2 import VCF
from collections import Counter

vcf = VCF("../data/annotated.vcf")

# Get all INFO fields from header
print("\nINFO fields from VCF header:")
for line in vcf.raw_header.split("\n"):
    if line.startswith("##INFO"):
        print(line)

# Try checking some known fields
clin_sigs = Counter()
allele_freqs = []

for i, variant in enumerate(vcf):
    if "CLIN_SIG" in variant.INFO:
        clin_sigs.update(str(variant.INFO.get("CLIN_SIG")).split(","))

    if "AF" in variant.INFO:
        allele_freqs.append(variant.INFO.get("AF"))

    if i > 1000:
        break

# Display some CLIN_SIG values
if clin_sigs:
    print("\nSample CLIN_SIG values:")
    for k, v in clin_sigs.most_common(10):
        print(f"  {k}: {v}")
else:
    print("\nNo CLIN_SIG values found in first 1000 variants.")

# Show AF range if present
if allele_freqs:
    print(f"\nSample AF values: {allele_freqs[:10]}")
else:
    print("\nNo AF values found in first 1000 variants.")
