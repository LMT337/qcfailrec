import csv
import argparse
parser = argparse.ArgumentParser()


parser.add_argument("file", type=str)

args = parser.parse_args()

outfile = args.file + '.reccomendation.tsv'

header = ['WorkOrder','date_QC','DNA','instrument_data_count','instrument_data_ids','WorkingDirectory','cram',
          'cram.md5','SAMPLE_ALIAS','ALIGNED_READS','ALIGNMENT_RATE','FIRST_OF_PAIR_MISMATCH_RATE',
          'SECOND_OF_PAIR_MISMATCH_RATE','Freemix_Alpha','GENOTYPING_CHIPMIX','HAPLOID_COVERAGE','PCT_10X',
          'PCT_20X','TOTAL_BASES_Q20_OR_MORE','discordant_rate','interchromosomal_rate','HET_SNP_Q',
          'HET_SNP_SENSITIVITY','MEAN_COVERAGE','MEAN_INSERT_SIZE','STANDARD_DEVIATION','PCT_ADAPTER','PF_READS',
          'PF_ALIGNED_BASES','TOTAL_PERCENT_DUPLICATION','TOTAL_READS','reads_mapped_as_singleton_percentage',
          'reads_mapped_in_proper_pairs_percentage','PF_HQ_ALIGNED_Q20_BASES','STATUS','Flagstats','QC Failed Metrics']

qc = {}

def topmed_metrics_fail(line):
    if (float(line['Freemix_Alpha']) >=  0.01):
        qc['qc_comment'] = 'Contamination'
        qc['qc_reccomendation'] = 'Library or DNA contaminated. Please abandon the library. Note: Source DNA may or may not be contaminated.'

# HAPLOID_COVERAGE < 30
# TOTAL_BASES_Q20_OR_MORE < 86,000,000,000
# PCT_10X < 0.95
# PCT_20X < 0.90
# GENOTYPING_CHIPMIX  = 0.01 < 0.9 (contamination)
# GENOTYPING_CHIPMIX = > 0.9 (wrong identity/sample swap)

list_format = []

with open(args.file) as infile, open( outfile, 'w') as outfilecsv:
    # print(infile)
    reader = csv.DictReader(infile, delimiter="\t")
    # print(reader)
    for line in reader:
        topmed_metrics_fail(line)
        print(qc)

exit()
