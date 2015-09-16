from abc import ABCMeta, abstractmethod

import zipfile
import pickle
from itertools import imap

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.feature_selection import VarianceThreshold

import config
from models.util import *

class Model(object):
    __metaclass__ = ABCMeta
     
    default_train_file = 'train_subset.pickle'
    default_test_file = 'test_subset.pickle'
    default_model_param_file = 'model_param.pickle'
    
    def __init__(self, **kwargs):
        self.verbose = kwargs.get('verbose', 1)

        if self.verbose:
            print 'Opening HTML zip file'
        self.__html_zip = zipfile.ZipFile(kwargs.get('html_cleaned_zip', config.html_cleaned_zip))
        
        self.__train_classes_filename = kwargs.get('train_file', self.default_train_file)
        self.__test_classes_filename = kwargs.get('test_file', self.default_test_file)

        self.__predict_classes_in_filename = kwargs.get('predict_in_file', None)
        self.__predict_classes_out_filename = kwargs.get('predict_out_file', None)
        
        self.__use_tfidf = kwargs.get('use_tfidx', False)
        self.__tfidf_transformer = None
        self.__use_variance_threshold = kwargs.get('use_variance_threshold', False)
        self.__variance_threshold = 0.8
        self.__variance_threshold_selector = None
        
        self.__model_param_filename = kwargs.get('model_param_file', self.default_model_param_file)

        self.__dtype = kwargs.get('dtype', np.float32)

        self.__filenames = []
        self.__contents = []
        self.__is_file_handle = True
        self.__class_vector = []

        if 'vocabulary_file' in kwargs:
            self.__vocabulary = sorted(load_pickle(kwargs['vocabulary_file']))
        else:
            self.__vocabulary = None
        self.__docmat = None
        
    def __load(self, filename, use_file_handles):
        self.__is_file_handle = use_file_handles
        
        if self.verbose:
            print 'Reading data'
            
        with open(filename, 'r') as pf:
            classes = pickle.load(pf)
            
        self.__file_names = classes.keys()
        self.__class_vector = np.empty(len(self.__file_names), dtype=self.__dtype)
        self.__content = []

        for i, f in enumerate(self.__file_names):
            self.__class_vector[i] = classes[f]

        def iterfn(f):
            if self.__is_file_handle:
                return self.__html_zip.open(f, 'r')
            else:
                with self.__html_zip.open(f, 'r') as zf:
                    return self.__content.append(zf.read())
                
        self.__contents = imap(iterfn, self.__file_names)

    def load_training_data(self, use_file_handles=True):
        self.__load(self.__train_classes_filename, use_file_handles)

    def load_testing_data(self, use_file_handles=True):
        self.__load(self.__test_classes_filename, use_file_handles)

    def load_prediction_data(self, use_file_handles=True):
        self.__load(self.__predict_classes_in_filename, use_file_handles)

    def save_prediction_data(self):
        if self.verbose:
            print 'Writing data'
            
        classes = {}
        for i, f in enumerate(self.__file_names):
            classes[f] = 1 if self.__class_vector[i] >= 0.5 else 0

        with open(self.__predict_classes_out_filename, 'w') as pf:
            pickle.dump(classes, pf, pickle.HIGHEST_PROTOCOL)
            
    def make_word_vectors(self):
        if self.verbose:
            print 'Computing word vectors'
            
        if self.__vocabulary is None:
            cv = CountVectorizer(stop_words=config.common_words,
                                 input=('file' if self.__is_file_handle else 'content'),
                                 dtype=self.__dtype)
            self.__docmat = cv.fit_transform(self.__contents)
            self.__vocabulary = cv.vocabulary_
        else:
            cv = CountVectorizer(stop_words=config.common_words,
                                 input=('file' if self.__is_file_handle else 'content'),
                                 dtype=self.__dtype,
                                 vocabulary=self.__vocabulary)
            self.__docmat = cv.transform(self.__contents)

        if self.__tfidf_transformer is None:
            if self.__use_tfidf:
                self.__tfidf_transformer = TfidfTransformer()
                self.__docmat = self.__tfidf_transformer.fit_transform(self.__docmat)
        else:
            self.__docmat = self.__tfidf_transformer.transform(self.__docmat)

        print 'BEFORE', self.__docmat.shape
        if self.__variance_threshold_selector is None:
            if self.__use_variance_threshold:
                self.__variance_threshold_selector = VarianceThreshold(self.__variance_threshold *
                                                                       (1.0 - self.__variance_threshold))
                self.__docmat = self.__variance_threshold_selector.fit_transform(self.__docmat)
        else:
            self.__docmat = self.__variance_threshold_selector.transform(self.__docmat)
        print 'AFTER ', self.__docmat.shape
            

    def get_document_matrix(self):
        return self.__docmat

    def get_document_class_vector(self):
        return self.__class_vector

    def set_document_class_vector(self, class_vector):
        self.__class_vector = class_vector

    @abstractmethod
    def getstate(self):
        return {'vocabulary':self.__vocabulary,
                'var_thresh_sel':self.__variance_threshold_selector}

    @abstractmethod
    def setstate(self, state):
        self.__vocabulary = state['vocabulary']
        self.__variance_threshold_selector = state['var_thresh_sel']

    def save(self):
        if self.verbose:
            print 'Saving model'
            
        with open(self.__model_param_filename, 'w') as pf:
            pickle.dump(self.getstate(), pf, pickle.HIGHEST_PROTOCOL)

    def load(self):
        if self.verbose:
            print 'Loading model'
            
        with open(self.__model_param_filename, 'r') as pf:
            state = pickle.load(pf)
            self.setstate(state)

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def test(self):
        pass

    @abstractmethod
    def predict(self):
        pass
