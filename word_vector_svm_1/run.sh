#!/bin/sh

export PYTHONPATH=$PYTHONPATH:/home/gautham/work/kaggle/truly_native/scripts

echo GENERATING SUBSETS
../gen_subset.py -n-train 30000 -n-test 3000

echo TRAINING
./train.py -in-train train_subset.pickle

echo TESTING
./test.py -in-test test_subset.pickle
