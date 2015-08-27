#!/usr/bin/env python

import pickle
import re
import sys
import random
import argparse
import models.config as cfg
from models import Model

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-in-train', type=str, default='train.pickle', help='Input training set dictionary')
    parser.add_argument('-out-train', type=str, default=Model.default_train_file, help='Output training set dictionary')
    parser.add_argument('-out-test', type=str, default=Model.default_test_file, help='Output training set dictionary')
    parser.add_argument('-n-train', type=int, default=10000, help='Number of training samples.')
    parser.add_argument('-n-test', type=int, default=100, help='Number of test samples.')

    return parser.parse_args()

def main():
    args = parse_args()
    
    with open(cfg.data_root + '/' + args.in_train, 'r') as pf:
        file_classes = pickle.load(pf)

    files = file_classes.keys()
    train_files = random.sample(files, args.n_train)
    test_files = random.sample(files, args.n_test)

    with open(args.out_train, 'w') as f:
        train = {f:file_classes[f] for f in train_files}
        pickle.dump(train, f, pickle.HIGHEST_PROTOCOL)
    
    with open(args.out_test, 'w') as f:
        test = {f:file_classes[f] for f in test_files}
        pickle.dump(test, f, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    main()
    
