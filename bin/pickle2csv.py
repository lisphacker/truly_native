#!/usr/bin/env python

import csv
import pickle
import sys

if len(sys.argv) != 4:
    sys.exit('SYNTAX: {0} <infile.csv> <infile.pickle> <outfile.csv>'.format(sys.argv[0]))

names = []
with open(sys.argv[1]) as f:
    csvreader = csv.reader(f)
    csvreader.next()

    for name, sponsored in csvreader:
        sponsored = sponsored == '1'
        names.append(name)

with open(sys.argv[2], 'r') as f:
    classes = pickle.load(f)

with open(sys.argv[3], 'w') as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(['file', 'sponsored'])

    for name in names:
        sponsored = 1 if classes[name] >= 0.5 else 0
        csvwriter.writerow([name, sponsored])


