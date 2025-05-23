# Variant Interpretation Pipeline
This project filters, analyzes, and visualizes variants from a VCF file (annotated using VEP). It focuses on variants in specific genes, regions, and clinical significance for downstream interpretation.
Goal: To analyze real VCF files using Ensembl VEP for variant interpretation as part of your genomics portfolio project.


## 🧪 Objective

To extract potentially pathogenic variants from a large annotated VCF file, focusing on:

- Specific genes (e.g., **BRCA1**, **BRCA2**, **TP53**)
- Genomic region(s)
- Allele frequency thresholds
- Clinical significance
- Zygosity and impact

## 📂 Project Structure
I created three folders data, results, scripts to oragnize all the files. 

## Initial Failed approach
Initial Approach was to Use Conda to Install Ensembl VEP. Therefore, 
- Installed Miniconda.
- Created a Conda environment and installed ensembl-vep from bioconda.
- Attempted to run vep (Variant Effect Predictor) in the terminal using this setup.

There were manyb pearl related issues with mutliple dependencies and then I switched to another method "Docker". But keep in mind, we need conda environment to run our multiple scripts in the project.

## Why Docker
- Docker provides isolated, pre-configured containers where all dependencies (including correct Perl and Python versions) are already set up and tested by Ensembl.
- Docker minimizes setup errors, avoids version conflicts, and is easier to reproduce across systems.

## Download the data
- Downloaded the VEP cache for homo_sapiens (Ensembl release 114, GRCh38), which was ~24.5 GB.

      vep_install -a c -s homo_sapiens -y GRCh38

- reused the annotated VCF data of the same genome that I created in another project (https://github.com/ubaid-mehmood0/Project-1-Variant-Calling-Pipeline-FASTQ-VCF-)
## Install Docker on Linux (Ubuntu/Debian)
### Install required packages
    sudo apt install \
	ca-certificates \
	curl \
	gnupg \
	lsb-release

### Add Docker’s GPG key & repository (use jammy)
The system Ubuntu I am using is latest and has a code name Noble. The codename noble corresponds to Ubuntu 24.04, which (as of now) is not yet officially supported by Docker’s stable repository. That’s why you're seeing: Package 'docker-ce' has no installation candidate.

We'll manually override the codename to use jammy (Ubuntu 22.04), which is supported and compatible.

* We can use the following lines of code all at once or individually copying and pasting. Even if we copy and paste all at once, the terminal still uses them individually. It's up to you. 

      sudo mkdir -p /etc/apt/keyrings
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
      sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

       echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
      https://download.docker.com/linux/ubuntu jammy stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

       sudo apt update
### Install Docker/ Engine
    sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
### Test the installation
    docker --version

    sudo docker run hello-world
## Pull Ensembl's VEP Docker Image
Use sudo everytime while using docker command unless you add yourself in Docker group.

    sudo docker pull ensemblorg/ensembl-vep

## Docker Command to Run VEP
* run the following at once

      sudo docker run \
      -u $(id -u):$(id -g) \
      -v ~/portfolio_projects/variant_interpretation/data:/data \
      ensemblorg/ensembl-vep \
      vep -i /data/annotated.vcf \
      -o /data/vep_output.vcf \
  	  --cache \
  	  --dir_cache /data \
  	  --offline \
  	  --species homo_sapiens \
  	  --assembly GRCh38 \
  	  --vcf \
  	  --force_overwrite

Ok VEP worked and now we have an updated annotated vcf file with VEP input in it.
### Check Your Output File
    head ~/portfolio_projects/variant_interpretation/data/vep_output.vcf
## Filtering Annotated VCF
Now filtering can be done on various basis or requirments its totally project /aim basis. But before that.
### Install cyvcf2
We’ll use Python with the pysam or cyvcf2 library to parse the VCF. Install dependencies first.

    sudo apt install -y build-essential autoconf libtool pkg-config zlib1g-dev libbz2-dev liblzma-dev libcurl4-openssl-dev

    pip install cyvcf2

### Execute python script for VEP-predicted IMPACT filtering
I used various scripts for filtering my desired aim.I executed filter_vep.py from the scripts folder. 

We are keeping variants that meet this condition. The VEP-predicted IMPACT is either:

- "HIGH" (e.g., frameshift, stop-gained)
- "MODERATE" (e.g., missense variant)

These impact levels are based on Ensembl's VEP annotations inside the CSQ field of your VCF file.

* Keep in mind filtering is based on the need of what I require from the VCF file. So python script has to vary from one condition to another. 

VCF file could have different headings to find the respective elements of particular gene or sequence of interest. So its better to get a good idea of how the VCF looks like and go through it. I used a script vcf_info.py for that but it can vary. 

We can adjust our filters to use the actual fields present:

- Gene name filtering → Extracted from the ANN field
- Effect types → Also from ANN (e.g., missense_variant, frameshift_variant, etc.)
- Zygosity → Can be extracted from the genotype field (variant.genotypes)
- No allele frequency or clinical significance filters can be applied unless we annotate those separately using tools like VEP, snpEff, or bcftools annotate with gnomAD.

After this, I executed another script filter_vep_2.py to get filtering further. 

VCF processed: 386,205 variants
Passed filters: 3 variants
Criteria used:
Gene in {BRCA1, BRCA2, TP53}
Annotation impact was MODERATE or HIGH

Further filtering was done based on the results I got above with 3 variants with the help of another script filter_vep_3.py. The result is as follows.
- Variants per gene: Counter({'BRCA1': 2, 'BRCA2': 1})
- Impact summary: Counter({'MODERATE': 3})
- Zygosity breakdown: Counter({'homozygous_alt': 3})

## Visualize/summarize the findings
Another script can be made based on the what we want in summary. I used another script export_summaries.py to prepare three CSV files:
- variants_per_gene.csv
- impact_summary.csv
- zygosity_breakdown.csv




