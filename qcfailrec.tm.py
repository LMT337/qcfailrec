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

qc_header = ['reason', 'qc_comment', 'qc_reccomendation']

qc = {}

def topmed_metrics_fail(line):
    if (float(line['Freemix_Alpha']) >=  0.01):
        qc['reason'] = 'Freemix_Alpha >= 0.01'
        qc['qc_comment'] = 'Contamination'
        qc['qc_reccomendation'] = 'Library or DNA contaminated. Please abandon the library. Note: Source DNA may or may not be contaminated.'
        print('Free True')

    elif (float(line['GENOTYPING_CHIPMIX'])  == 0.01 or  float(line['GENOTYPING_CHIPMIX']) < 0.9):
        qc['reason'] = 'genotyping_chipmix equal to 0.01 or less than 0.9'
        qc['qc_comment'] = 'Contamination'
        qc['qc_reccomendation'] = 'Library or DNA contaminated. Please abandon the library. Note: Source DNA may or may not be contaminated.'
        print('GT-True')
    elif (float(line['GENOTYPING_CHIPMIX']) >=  0.9):
        qc['reason'] = 'genotyping_chipmix greater than 0.9'
        qc['qc_comment'] = 'metrics indicate wrong identity/sample swap'
        qc['qc_reccomendation'] = 'Possible library/DNA swap, needs further investigation starting with QC'
        print('GTother-True')

    elif (float(line['GENOTYPING_CHIPMIX']) >= 0.9):
        qc['reason'] = 'genotyping_chipmix greater than 0.9'
        qc['qc_comment'] = 'Coverage fail'
        qc['qc_reccomendation'] = 'Possible library/DNA swap, needs further investigation starting with QC'
        print('GTother-True')

    elif (float(line['HAPLOID_COVERAGE']) < 30 or float(line['TOTAL_BASES_Q20_OR_MORE']) < 86
          or float(line['PCT_10X']) < 0.95 or float(line['PCT_20X']) < 0.90):
        print('hello')

with open(args.file) as infile, open( outfile, 'w') as outfilecsv:
    reader = csv.DictReader(infile, delimiter="\t")

    header_fields = header + qc_header
    w = csv.DictWriter(outfilecsv, header_fields, delimiter="\t")
    w.writeheader()

    for line in reader:
        topmed_metrics_fail(line)
        results = dict(list(line.items()) + list(qc.items()))
        w.writerow(results)


exit()
