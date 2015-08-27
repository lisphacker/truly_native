from model import Model

from sklearn.svm import SVC

class WordVectorSVM(Model):
    def __init__(self, **kwargs):
        Model.__init__(self, **kwargs)

        self.__svc = None

    def getstate(self):
        state = Model.getstate(self)
        state['svc'] = self.__svc
        return state
    
    def setstate(self, state):
        self.__svc = state['svc']
        Model.setstate(self, state)
        
    def train(self):
        self.load_training_data()
        self.make_word_vectors()

        if self.verbose:
            print 'Fitting SVM'
        docmat = self.get_document_matrix()
        class_vector = self.get_document_class_vector()

        self.__svc = SVC()
        self.__svc.fit(docmat, class_vector)

    def test(self):
        self.load_training_data()
        self.make_word_vectors()

        docmat = self.get_document_matrix()
        class_vector_ref = self.get_document_class_vector()

        if self.verbose:
            print 'Predicting classes'
        class_vector_test = self.__svc.predict(docmat)

        print 'Evaluating results'
        total_count = 0
        match_count = 0
        for ref, test in zip(class_vector_ref, class_vector_test):
            refb = ref >= 0.5
            testb = test >= 0.5

            if refb == testb:
                match_count += 1
            total_count += 1

        print 'Success rate =', (match_count * 100.0) / total_count

    def predict(self):
        self.load_prediction_data()
        self.make_word_vectors()

        docmat = self.get_document_matrix()

        if self.verbose:
            print 'Predicting classes'
        class_vector = self.__svc.predict(docmat)

        self.set_document_class_vector(class_vector)

        self.save_prediction_data()
