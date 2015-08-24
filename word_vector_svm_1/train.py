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

    parser.add_argument('-in-train', type=str, default='train.pickle', help='Input training set dictionary')
    parser.add_argument('-out-model-param', type=str, default='model_param.pickle', help='Model parameters')

    return parser.parse_args()

def main():
    args = parse_args()

    with open(args.in_train, 'r') as pf:
        file_classes = pickle.load(pf)

    zin = zipfile.ZipFile(cfg.html_cleaned_zip, 'r')

    files = []
    class_vector = np.empty(len(file_classes), dtype=np.float32)
    
    for i, (filename, sponsored) in enumerate(file_classes.iteritems()):
        with zin.open(filename, 'r') as f:
            files.append(f.read())
        class_vector[i] = float(sponsored)

    cv = CountVectorizer(input='content', strip_accents='ascii', stop_words='english', lowercase=False, dtype=np.float32)
    docmat = cv.fit_transform(files)

    svc = SVC()
    svc.fit(docmat, class_vector)

    with open(args.out_model_param, 'w') as f:
        pickle.dump((cv.vocabulary_, svc), f, pickle.HIGHEST_PROTOCOL)
    
    
        
        
if __name__ == '__main__':
    main()
