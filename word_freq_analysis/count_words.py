#!/usr/bin/env python

import zipfile
import pickle

from Queue import Queue

import models.config as cfg

def generate_word_count(zin, classes):
    all_word_freq = {}
    sponsored_word_freq = {}
    organic_word_freq = {}
    page_word_freq = {}


    names = zin.namelist()
    #names = names[0:10000]

    print 'Generating word count'
    for i, fn in enumerate(names):
        words = None
        with zin.open(fn) as f:
            words = f.read().split(' ')

        freq = {}

        ## if fn in classes:
        ##     if classes[fn]:
        ##         cls_freq = sponsored_word_freq
        ##     else:
        ##         cls_freq = organic_word_freq
        ## else:
        ##     cls_freq = None
    
        for word in words:
            ## all_word_freq[word] = all_word_freq.get(word, 0) + 1
            freq[word] = freq.get(word, 0) + 1

            ## if cls_freq is not None:
            ##     cls_freq[word] = cls_freq.get(word, 0) + 1

        page_word_freq[fn] = freq

        print '{0}/{1}'.format(i + 1, len(names))

    return all_word_freq, sponsored_word_freq, organic_word_freq, page_word_freq


def main():
    print 'Opening ZIP file'
    zin = zipfile.ZipFile(cfg.html_cleaned_zip, 'r')
    with open(cfg.train_classes_file) as f:
        classes = pickle.load(f)

    all_word_freq, sponsored_word_freq, organic_word_freq, page_word_freq = generate_word_count(zin, classes)

    print 'Saving frequency file'
    with open(cfg.word_freq_file, 'w') as pf:
        pickle.dump((all_word_freq, sponsored_word_freq, organic_word_freq, page_word_freq), pf, pickle.HIGHEST_PROTOCOL)

def main2():
    print 'Opening ZIP file'
    zin = zipfile.ZipFile(cfg.html_cleaned_zip, 'r')
    with open(cfg.train_classes_file) as f:
        classes = pickle.load(f)

    all_word_freq, sponsored_word_freq, organic_word_freq, page_word_freq = generate_word_count(zin, classes)

    zout = zipfile.ZipFile('page_word_count.zip', 'w', zipfile.ZIP_DEFLATED, True)

    print 'Saving frequency file'
    temp_pickle = '/tmp/page_word_count.pickle'
    l = len(page_word_freq.keys())
    for i, fn in enumerate(page_word_freq):
        with open(temp_pickle, 'w') as f:
            pickle.dump(page_word_freq[fn], f, pickle.HIGHEST_PROTOCOL)
        del page_word_freq[fn]
            
        print '{0}/{1}'.format(i + 1, l)
        
        zout.write(temp_pickle, fn + '.pickle')

        
    zin.close()
    zout.close()

if __name__ == '__main__':
    #main()
    pass
