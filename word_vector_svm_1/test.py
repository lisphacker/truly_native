#!/usr/bin/env python

import pickle
import argparse
import zipfile
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
import numpy as np
import cfg


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-in-test', type=str, default='test.pickle', help='Input test set dictionary')
    parser.add_argument('-in-model-param', type=str, default='model_param.pickle', help='Model parameters')

    return parser.parse_args()

def main():
    args = parse_args()

    with open(args.in_test, 'r') as pf:
        file_classes = pickle.load(pf)

    zin = zipfile.ZipFile(cfg.html_cleaned_zip, 'r')

    files = []
    class_vector_ref = np.empty(len(file_classes), dtype=np.float32)
    
    print 'Reading files'    
    for i, (filename, sponsored) in enumerate(file_classes.iteritems()):
        with zin.open(filename, 'r') as f:
            files.append(f.read())
        class_vector_ref[i] = float(sponsored)

    with open(args.in_model_param, 'r') as pf:
        vocabulary, svc = pickle.load(pf)
    
    print 'Generating word vector'
    cv = CountVectorizer(input='content', strip_accents='ascii', stop_words='english', lowercase=False,
                         vocabulary=vocabulary, dtype=np.float32)
    docmat = cv.transform(files)

    print 'Predicting'
    class_vector = svc.predict(docmat)

    print 'Evaluating results'
    total_count = 0
    match_count = 0
    for ref, test in zip(class_vector_ref, class_vector):
        refb = ref >= 0.5
        testb = test >= 0.5

        if refb == testb:
            match_count += 1
        total_count += 1

    print 'Success rate =', (match_count * 100.0) / total_count
        
if __name__ == '__main__':
    main()
