#!/usr/bin/env python

import zipfile
import numpy as np
import pickle
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from models import *
import models.config as cfg

def izip(z, filenames):
    for fn in filenames:
        f = z.open(fn, 'r')
        yield f
        f.close()

def main():
    print 'Opening ZIP file'
    zin = zipfile.ZipFile(config.html_cleaned_zip, 'r')

    filenames = zin.namelist()
    filenames = filenames[0:10]
    filenames.sort()

    print 'Reading ZIP file'
    ordering = {n:i for i, n in enumerate(filenames)}
    #contents = [zin.open(n, 'r') for n in filenames]

    cv = CountVectorizer(stop_words=config.common_words,
                         input='file',
                         dtype=np.float32)
    print 'Learning vocabulary'
    cv.fit(izip(zin, filenames))
    vocabulary = cv.vocabulary_
    
    print 'Generating word vectors'
    docmat1 = cv.transform(izip(zin, filenames))

    print 'Generating TF-IDF word vectors'
    docmat2 = TfidfTransformer().fit_transform(docmat1)

    print 'Writing output'
    with open(config.html_config, 'w') as pf:
        pickle.dump((filenames, ordering, vocabulary), pf, pickle.HIGHEST_PROTOCOL)

    np.savez(config.doc_mat, plain=docmat1, tfidf=docmat2)

if __name__ == '__main__':
    main()
