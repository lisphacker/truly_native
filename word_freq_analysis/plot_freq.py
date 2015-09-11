#!/usr/bin/env python

import pickle
from collections import namedtuple
import matplotlib.pyplot as plt

import models.config as cfg
from models.util import *

WordFreq = namedtuple('WordFreq', ['word', 'count'])

def process_global_word_freq(wfd, color):
    wfl = [WordFreq(w, wfd[w]) for w in wfd]
    wfl = sorted(wfl, cmp=lambda x, y: cmp(x.count, y.count), reverse=True)

    print 'Len =', len(wfl)

    #for wf in wfl:
    #    print wf.word, wf.count

    plt.plot([wf.count for wf in wfl], color=color)
    
def main():

    plt.figure()
    process_global_word_freq(all_word_freq, 'b')
    process_global_word_freq(sponsored_word_freq, 'r')
    process_global_word_freq(organic_word_freq, 'g')
    plt.show()

if __name__ == '__main__':
    main()
