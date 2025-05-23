import csv
from collections import Counter

# Example summary data (replace these with your actual data if using separately)
variants_per_gene = Counter({'BRCA1': 2, 'BRCA2': 1})
impact_summary = Counter({'MODERATE': 3})
zygosity_breakdown = Counter({'homozygous_alt': 3})

# Output directory
output_dir = "../results"

# Save function
def save_counter_to_csv(counter, filename, fieldnames):
    with open(f"{output_dir}/{filename}", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key, count in counter.items():
            writer.writerow({fieldnames[0]: key, fieldnames[1]: count})

# Export each summary
save_counter_to_csv(variants_per_gene, "variants_per_gene.csv", ["Gene", "Variant_Count"])
save_counter_to_csv(impact_summary, "impact_summary.csv", ["Impact_Level", "Count"])
save_counter_to_csv(zygosity_breakdown, "zygosity_breakdown.csv", ["Zygosity_Type", "Count"])

print("CSV files exported to results folder.")
