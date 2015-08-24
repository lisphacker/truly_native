#!/usr/bin/env python

import csv
import pickle
import cfg

train = {}
with open(cfg.data_root + '/train.csv') as f:
    csvreader = csv.reader(f)
    csvreader.next()

    for name, sponsored in csvreader:
        sponsored = sponsored == '1'
        train[name] = sponsored


with open(cfg.data_root + '/train.pickle', 'w') as f:
    pickle.dump(train, f, pickle.HIGHEST_PROTOCOL)

