This is a script that takes indexed bam files (as delimited by example_config.txt),
and generates a single-file track for all of the bam files that can be easily
uploaded and viewed on UCSC Genome Browser.

Requirements:
Python 3+
Pandas

When run the user will be prompted with two questions:
1. Chromosome location
    - Input a chromosomal location like this: chr17:70,844,205-70,851,210
2. Gene of interest
    - This is merely for track nomenclature - any single-word name works
