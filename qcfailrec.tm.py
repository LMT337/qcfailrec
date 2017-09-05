import csv
import argparse
parser = argparse.ArgumentParser()


parser.add_argument("file", type=str)

args = parser.parse_args()
outfile = args.file + '.reccomendation.tsv'

def topmed_metrics_fail(line):


with open(args.file) as infile, open( outfile, 'w') as outfilecsv:
    print(infile)
    reader = csv.DictReader(infile, delimiter="\t")
    print(reader)
    for line in reader:
        topmed_metrics_fail(line)
exit()
