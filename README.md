# Functionality  
This is a script that takes indexed bam files (as delimited by ucsc_config.txt),
and generates a single-file track for all of the bam files that can be easily
uploaded and viewed on UCSC Genome Browser in the event that one doesn't have a
public server on which to host a large bigwig file.


![Image of browser](https://i.imgur.com/Y1noBTG.png)

# Dependencies  
Python 3+  
Pandas


# How to Run it  
When run the user will be prompted with two questions:
1. Chromosome location
    - Input a chromosomal location like this: chr17:70,844,205-70,851,210
2. Gene of interest
    - This is merely for track nomenclature - any single-word name works

# Before you start  
You need to configure your ucsc_config.txt file to have three columns:  
1. Sample name
2. Bam name (must match the name of the bam file exactly)
3. Normalized read depth  
4. Color - this should be in 'R.G.B.' format. Alternatively, leave at '0' and
   it will generate random colors for each track.

normalized_read_depth is calculated by getting read depth from the bam file
followed by dividing by 1x10^6.  
Get read depth using:  
samtools view -F 0x4 foo.sorted.bam | cut -f 1 | uniq | wc -l
