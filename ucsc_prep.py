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

if location == '' or filename == '':
	print('Please input valid location or gene name')
	sys.exit()

bam_df = pd.read_csv('ucsc_config.txt', sep=',', header='infer')

bam_df['sample_name'] = bam_df['sample_name'].astype(str)

# Generating the tracknames
bam_df['track_name'] = bam_df['sample_name']

# In the event that a bam file in a different directory is inputted:
bam_df['clean_bam_name'] = bam_df.bam_name.str.split('/').str[-1]

# Checking if there's color, and adding some if there isn't
if list(set(list(bam_df['color'])))[0] == 0:
	howmanycolors = bam_df.shape[0]
	bam_df['color'] = generate_rand_colors(howmanycolors)
else:
	bam_df['color'] = bam_df['color'].str.replace('.',',')

# Going through each file
for idx, row in bam_df.iterrows():

    # Generating the smaller bam file
    os.system('samtools view -bh %s %s > %s_temp_for_prog%s' %
              (row['bam_name'], location, filename, row['clean_bam_name']))

    # Generating the bedgraph
    os.system("""bedtools genomecov -split -ibam %s_temp_for_prog%s -bg -scale %s > \
              %s_%s.temp.bedgraph""" %
              (filename, row['clean_bam_name'], row['normalized_read_depth'],filename, row['clean_bam_name']))

    # Generating the head file that we will add to the final product
    header_file = open("%s_%s_header.txt" % (filename, row['clean_bam_name'].split('.b')[0]), 'w')
    header_file.write("""track type="bedGraph" name="%s" color=%s \
                      visibility=full autoScale=off maxHeightPixels=100:30:11 \
                      viewLimits=0.0:1.5\nbrowser position %s\n"""
                      % (row['track_name'], row['color'], location))
    header_file.close()

    # Catting all of the bedgraphs to the same file
    if idx == 0:
        os.system("""cat %s_%s_header.txt %s_%s.temp.bedgraph > \
                  %s.bedgraph"""
                  % (filename, row['clean_bam_name'].split('.b')[0], filename, row['clean_bam_name'], filename))
    else:
        os.system("""cat %s_%s_header.txt %s_%s.temp.bedgraph >> \
                  %s.bedgraph"""
                  % (filename, row['clean_bam_name'].split('.b')[0], filename, row['clean_bam_name'], filename))

    # Removing the header and temporary files to reduce clutter:
    os.system('rm %s_temp_for_prog%s' % (filename, row['clean_bam_name']))
    os.system('rm %s_%s.temp.bedgraph' % (filename, row['clean_bam_name']))
    os.system('rm %s_%s_header.txt' % (filename, row['clean_bam_name'].split('.b')[0]))
