#!/bin/sh

export PYTHONPATH=$PYTHONPATH:..

../gen_subset.py
./train.py -in-train train_subset.pickle
#./test.py -in-test test_subset.pickle
