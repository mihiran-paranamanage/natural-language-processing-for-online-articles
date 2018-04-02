from cse_site.settings import CSE_ROOT
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from nltk.stem.snowball import SnowballStemmer
import sklearn.datasets
import numpy as np
import glob
import os

class StemmedCountVectorizer(CountVectorizer):
    
    def build_analyzer(self):
        stemmer = SnowballStemmer("english")
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: ([stemmer.stem(word) for word in analyzer(doc)])

class Categorizer:

    def __init__(self):
        pass

    def categorize(self, content):
        '''
        input: content of a article
        output: category of the article
        '''
        categories = ['awards', 'expansion', 'financing', 'production', 'others']
        train_data, train_target = [], []
        # data preparation
        for category in categories:
            files = glob.glob(CSE_ROOT + '/train_data/%s/%s_*' % (category, category))
            for file in files:
                f = open(file, "r", encoding="utf8")
                if f:
                    train_data.append(f.read())
                    train_target.append(category)
        # create train dataset
        train_dataset = sklearn.datasets.base.Bunch(data=train_data, target=train_target)
        # support vector machine
        text_clf_svm = Pipeline([
                                ('vect', StemmedCountVectorizer(stop_words='english')),
                                ('tfidf', TfidfTransformer()),
                                ('clf-svm', SGDClassifier())
                                ])
        # train
        text_clf_svm = text_clf_svm.fit(train_dataset.data, train_dataset.target)
        # predict
        predicted_svm = text_clf_svm.predict([content])
        # return svm result
        return predicted_svm[0]
