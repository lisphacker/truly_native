#!/usr/bin/env python

import zipfile
import pickle

from Queue import Queue
from thread import start_new_thread

import models.config as cfg

def generate_word_count(zin, q):
    names = zin.namelist()
    #names = names[0:100]

    print 'Generating word count'
    lastpc = -1
    for i, fn in enumerate(names):
        words = None
        with zin.open(fn) as f:
            words = f.read().split(' ')

        freq = {}

        for word in words:
            freq[word] = freq.get(word, 0) + 1

        q.put((fn, freq))

        pc = int((100.0 * (i + 1)) / len(names))
        if pc != lastpc:
            print pc, '%'
            lastpc = pc

    q.put((None, None))

def main():
    print 'Opening ZIP file'
    zin = zipfile.ZipFile(cfg.html_cleaned_zip, 'r')
    with open(cfg.train_classes_file) as f:
        classes = pickle.load(f)

    q = Queue()
    start_new_thread(generate_word_count, (zin, q))
    
    zout = zipfile.ZipFile('page_word_count.zip', 'w', zipfile.ZIP_DEFLATED, True)

    print 'Saving frequency file'
    temp_pickle = '/tmp/page_word_count.pickle'

    while True:
        fn, freq = q.get()
        if fn is None:
            break

        with open(temp_pickle, 'w') as f:
            pickle.dump(freq, f, pickle.HIGHEST_PROTOCOL)
            
        zout.write(temp_pickle, fn + '.pickle')

    zin.close()
    zout.close()

if __name__ == '__main__':
    #main()
    pass
