#!/bin/sh

echo GENERATING SUBSETS
gen_subset.py -n-train 1000 -n-test 1000

#echo TRAINING
#time run.py -model WordVectorSVM -model-params "use_tfidf=True" -train

echo TESTING
time run.py -model WordVectorSVM -model-params "use_tfidf=True" -test

#echo PREDICTING
#time run.py -model WordVectorSVM -predict \
#    -predict-in-file ../../data/sampleSubmissionOriginal.pickle \
#    -predict-out-file ../../data/sampleSubmission.pickle 
