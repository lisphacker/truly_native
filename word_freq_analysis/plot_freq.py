#!/usr/bin/env python

from collections import namedtuple
import matplotlib.pyplot as plt

import models.config as cfg
from models.util import *

WordCount = namedtuple('WordCount', ['word', 'count'])

def process_global_word_count(wcd, color):
    wcl = [WordCount(w, wcd[w]) for w in wcd]
    wcl = sorted(wcl, cmp=lambda x, y: cmp(x.count, y.count), reverse=True)

    print 'Len =', len(wcl)

    #for wc in wcl:
    #    print wc.word, wc.count

    plt.plot([wc.count for wc in wcl], color=color)
    
def main():
    print 'Loading file'
    all_word_count = load_pickle(cfg.all_word_count_file)
    sponsored_word_count = load_pickle(cfg.sponsored_word_count_file)
    organic_word_count = load_pickle(cfg.organic_word_count_file)

    print 'Plotting word counts'    
    plt.figure()
    process_global_word_count(all_word_count, 'b')
    process_global_word_count(sponsored_word_count, 'r')
    process_global_word_count(organic_word_count, 'g')
    plt.show()

if __name__ == '__main__':
    #main()
    pass
