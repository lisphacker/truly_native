#!/usr/bin/env python

import csv
import pickle
import sys

if len(sys.argv) != 3:
    sys.exit('SYNTAX: {0} <infile.csv> <outfile.pickle>'.format(sys.argv[0]))
    
train = {}
with open(sys.argv[1]) as f:
    csvreader = csv.reader(f)
    csvreader.next()

    for name, sponsored in csvreader:
        sponsored = sponsored == '1'
        train[name] = sponsored


with open(sys.argv[2], 'w') as f:
    pickle.dump(train, f, pickle.HIGHEST_PROTOCOL)

