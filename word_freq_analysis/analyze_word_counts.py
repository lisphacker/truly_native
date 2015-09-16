#!/usr/bin/env python

from collections import namedtuple
import matplotlib.pyplot as plt

import models.config as cfg
from models.util import *

WordCount = namedtuple('WordCount', ['word', 'count'])

def filter_wc_range(wcd, min_, max_):
    return {w:wcd[w] for w in filter(lambda w: wcd[w] >= min_ and wcd[w] <= max_, wcd)}

def filter_wc(wcd, fn):
    return {w:wcd[w] for w in filter(fn, wcd)}

def load_data():
    all_word_count = load_pickle(cfg.all_word_count_file)
    sponsored_word_count = load_pickle(cfg.sponsored_word_count_file)
    organic_word_count = load_pickle(cfg.organic_word_count_file)

    return (all_word_count, sponsored_word_count, organic_word_count)

def main():
    print 'Loading file'
    all_word_count, sponsored_word_count, organic_word_count = load_data()

    print len(all_word_count), len(sponsored_word_count), len(organic_word_count)
    print 'Filtering word counts'
    all_word_count = filter_wc_range(all_word_count, 8000, 666000)
    sponsored_word_count = filter_wc_range(sponsored_word_count, 2000, 95000)
    organic_word_count = filter_wc_range(organic_word_count, 8000, 250000)

    print len(all_word_count), len(sponsored_word_count), len(organic_word_count)

if __name__ == '__main__':
    #main()
    pass
