import os
import sys
from cyvcf2 import VCF, Writer

# Paths
INPUT_VCF = "../results/vep_output.vcf"
OUTPUT_VCF = "../results/filtered_vep_output.vcf"

# Define filtering function
def passes_filters(record):
    """
    Filters variants based on VEP consequence annotations.
    Modify this function as needed to apply custom filters.
    """
    csq = record.INFO.get("CSQ")
    if not csq:
        return False

    for entry in csq.split(','):
        fields = entry.split('|')
        consequence = fields[1] if len(fields) > 1 else ""
        impact = fields[2] if len(fields) > 2 else ""

        # Customize logic below — here we keep variants with HIGH or MODERATE impact
        if impact in ("HIGH", "MODERATE"):
            return True
    return False

def main():
    if not os.path.exists(INPUT_VCF):
        print(f"ERROR: Input VCF not found at {INPUT_VCF}")
        sys.exit(1)

    vcf_in = VCF(INPUT_VCF)
    vcf_out = Writer(OUTPUT_VCF, vcf_in)

    kept = 0
    total = 0

    for record in vcf_in:
        total += 1
        if passes_filters(record):
            vcf_out.write_record(record)
            kept += 1

    vcf_in.close()
    vcf_out.close()

    print(f"Finished filtering: {kept}/{total} variants kept.")
    print(f"Filtered VCF saved to: {OUTPUT_VCF}")

if __name__ == "__main__":
    main()
