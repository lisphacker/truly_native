#!/usr/bin/env python

import zipfile
import pickle
import numpy as np
import models.config as cfg
import random

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline

def main():
    zin = zipfile.ZipFile(cfg.html_cleaned_zip, 'r')

    with open('train_subset.pickle', 'r') as pf:
        train = pickle.load(pf)

    print 'Num training samples: ', len(train)
    
    train_names = sorted(train.keys())
    train_classes = np.array([train[n] for n in train_names], dtype=np.float32)

    pipeline = Pipeline([('vect', CountVectorizer(dtype=np.float32)),
                         ('tfidf', TfidfTransformer()),
                         ('clf', SGDClassifier())])
    parameters = {
        #'vect__max_df': (0.5, 0.75, 1.0),
        'vect__max_df': (0.5, 0.75),
        
        'vect__max_features': (None, 5000, 10000, 50000),
        #'vect__max_features': (5000,),
        
        'vect__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
        #'vect__ngram_range': ((1, 1),),
        
        #'tfidf__norm': ('l1', 'l2'),
        'tfidf__norm': ('l2', ),
        
        #'clf__alpha': (0.0001, 0.00001, 0.000001),
        'clf__alpha': (0.0001,),
        
        #'clf__penalty': ('l2', 'elasticnet'),
        'clf__penalty': ('l2',),
        
        #'clf__n_iter': (5, 10, 50, 80),
        'clf__n_iter': (5,),
        
    }

    def read_file(fn):
        with zin.open(fn, 'r') as f:
            return f.read()
    
    train_data = map(read_file, train_names)

    grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1)

    grid_search.fit(train_data, train_classes)

    best_parameters = grid_search.best_estimator_.get_params()
    print 'Best parameters:'
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))

if __name__ == '__main__':
    main()
    
