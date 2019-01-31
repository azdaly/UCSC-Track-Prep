import os
import pandas as pd
import random


def generate_rand_colors(how_many):
    random_colors = []
    for item in list(range(how_many)):
        temp_list = []
        for second_item in list(range(3)):
            temp_rand = random.randint(0, 129)
            temp_list.append(temp_rand)
        random_colors.append('%s,%s,%s' % (str(temp_list[0]),
                                           str(temp_list[1]),
                                           str(temp_list[2])))

    return random_colors


location = input("Please input chromosomal location:   ")
filename = input('Which gene are you looking at?  ')

bam_df = pd.read_csv('ucsc_config.txt', sep=',', header='infer', )

bam_df['sample_name'] = bam_df['sample_name'].astype(str)

# Generating the tracknames
bam_df['track_name'] = bam_df['sample_name'] + filename

# Adding a color column
howmanycolors = bam_df.shape[0]
bam_df['color'] = generate_rand_colors(howmanycolors)

# Going through each file
for idx, row in bam_df.iterrows():

    # Generating the smaller bam file
    os.system('samtools view -bh %s %s > temp_for_prog%s' %
              (row['bam_name'], location, row['bam_name']))

    # Generating the bedgraph
    os.system("""bedtools genomecov -ibam temp_for_prog%s -bg -scale %s > \
              %s.temp.bedgraph""" %
              (row['bam_name'], row['normalized_read_depth'], row['bam_name']))

    # Generating the head file that we will add to the final product
    header_file = open("%s_header.txt" % row['bam_name'].split('.b')[0], 'w')
    header_file.write("""track type="bedGraph" name="%s" color=%s \
                      visibility=full autoScale=off maxHeightPixels=100:50:11 \
                      viewLimits=0.0:1.5\nbrowser position %s\n"""
                      % (row['track_name'], row['color'], location))
    header_file.close()

    # Catting all of the bedgraphs to the same file
    if idx == 0:
        os.system("""cat %s_header.txt %s.temp.bedgraph > \
                  %s.bedgraph"""
                  % (row['bam_name'].split('.b')[0], row['bam_name'], filename))
    else:
        os.system("""cat %s_header.txt %s.temp.bedgraph >> \
                  %s.bedgraph"""
                  % (row['bam_name'].split('.b')[0], row['bam_name'], filename))

    # Removing the header and temporary files to reduce clutter:
    os.system('rm temp_for_prog%s' % row['bam_name'])
    os.system('rm %s.temp.bedgraph' % row['bam_name'])
    os.system('rm %s_header.txt' % row['bam_name'].split('.b')[0])
