#!/usr/bin/env python

import pickle
import argparse
import zipfile
import cfg


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-in-train', type=str, default='train.pickle', help='Input training set dictionary')
    parser.add_argument('-out-organic-set', type=str, default='organic.pickle', help='Organic word set')
    parser.add_argument('-out-sponsored-set', type=str, default='sponsored.pickle', help='Sponsored word set')

    return parser.parse_args()

def main():
    args = parse_args()

    with open(args.in_train, 'r') as pf:
        file_classes = pickle.load(pf)

    zin = zipfile.ZipFile(cfg.data_root + '/html_cleaned.zip', 'r')

    common_organic_words = None
    common_sponsored_words = None

    for filename, sponsored in file_classes.iteritems():
        with zin.open(filename, 'r') as f:
            words = set(f.read().split())

        common_words = common_sponsored_words if sponsored else common_organic_words

        if common_words is None:
            common_words = words
        else:
            common_words &= words

        if sponsored:
            common_sponsored_words = words
        else:
            common_organic_words = words

    with open(args.out_organic_set, 'w') as f:
        pickle.dump(common_organic_words, f, pickle.HIGHEST_PROTOCOL)
        
    with open(args.out_sponsored_set, 'w') as f:
        pickle.dump(common_sponsored_words, f, pickle.HIGHEST_PROTOCOL)
        
if __name__ == '__main__':
    main()
