#!/bin/sh

#echo GENERATING SUBSETS
#gen_subset.py -n-train 100 -n-test 10000

#echo TRAINING
#time run.py -model WordVectorSVM -train

#echo TESTING
#time run.py -model WordVectorSVM -test

echo PREDICTING
time run.py -model WordVectorSVM -predict \
    -predict-in-file ../../data/sampleSubmissionOriginal.pickle \
    -predict-out-file ../../data/sampleSubmission.pickle 
