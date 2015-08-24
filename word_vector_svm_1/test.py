#!/usr/bin/env python

import pickle
import argparse
import zipfile
import cfg


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-in-test', type=str, default='test.pickle', help='Input training set dictionary')
    parser.add_argument('-in-organic-set', type=str, default='organic.pickle', help='Organic word set')
    parser.add_argument('-in-sponsored-set', type=str, default='sponsored.pickle', help='Sponsored word set')

    return parser.parse_args()

def main():
    args = parse_args()

    with open(args.in_test, 'r') as pf:
        file_classes = pickle.load(pf)

    with open(args.in_organic_set, 'r') as pf:
        common_organic_words = pickle.load(pf)
        
    with open(args.in_sponsored_set, 'r') as pf:
        common_sponsored_words = pickle.load(pf)

    zin = zipfile.ZipFile(cfg.data_root + '/html_cleaned.zip', 'r')

    total_count = 0
    match_count = 0
    for filename, sponsored_ref in file_classes.iteritems():
        with zin.open(filename, 'r') as f:
            words = set(f.read().split())

        sponsored = len(words & common_organic_words) < len(words & common_sponsored_words)

        if sponsored == sponsored_ref:
            match_count += 1
        total_count += 1
            

    print 'Success rate: ', (100.0 * match_count) / total_count
        
if __name__ == '__main__':
    main()
