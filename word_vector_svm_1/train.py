#!/usr/bin/env python

import pickle
import argparse
import zipfile
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import cfg


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-in-train', type=str, default='train.pickle', help='Input training set dictionary')
    parser.add_argument('-out-model-param', type=str, default='model_param.pickle', help='Model parameters')

    return parser.parse_args()

def main():
    args = parse_args()

    with open(args.in_train, 'r') as pf:
        file_classes = pickle.load(pf)

    zin = zipfile.ZipFile(cfg.html_cleaned_zip, 'r')

    ## initial_word_index = {}

    ## max_count = len(file_classes.keys()) * 20
    
    ## for filename, sponsored in file_classes.iteritems():
    ##     with zin.open(filename, 'r') as f:
    ##         words = f.read().split()

    ##     for word in words:
    ##         if word in cfg.common_words or len(word) > cfg.max_word_len:
    ##             continue

    ##         if word not in initial_word_index:
    ##             initial_word_index[word] = 1
    ##         else:
    ##             initial_word_index[word] += 1

    ## word_index = {word:initial_word_index[word] for word in
    ##               filter(lambda word: initial_word_index[word] > 2 and initial_word_index[word] < max_count,
    ##                      initial_word_index)}

    ## print len(initial_word_index.keys())
    ## print len(word_index.keys())

    files = []
    for filename, sponsored in file_classes.iteritems():
        with zin.open(filename, 'r') as f:
            files.append(f.read())

    cv = CountVectorizer(input='content', strip_accents='ascii', stop_words='english', lowercase=False, dtype=np.float32)
    dm = cv.fit_transform(files)
    print dm.shape, dm.dtype, type(dm)
        
        
if __name__ == '__main__':
    main()
