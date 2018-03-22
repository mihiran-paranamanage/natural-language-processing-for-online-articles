from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

class Categorizer:

    def __init__(self):
        pass

    def categorize(self, content):
        '''
        input: content of a article
        output: category of the article
        '''
        # data preparation
        '''
        add related keywords for corresponding categories of the data_set.
        make sure that all categories have the same number of keywords, to get better result.
        '''
        data_set = [('position vision mission goal objective authority capital', 'position'),
                    ('award win won ceremony congratulation congratulate honour', 'award'),
                    ('expansion new branch bureau division office section', 'expansion'),
                    ('finance investment asset contribution five six seven', 'finance'),
                    ('production products goods four five six seven', 'production'),
                    ('quality good product four five six seven', 'quality'),
                    ('merchandising marketing three four five six seven', 'merchandising'),
                    ('corporate social responsibility four five six seven', 'csr')]
        # feature extraction
        all_features = set(word.lower() for data in data_set for word in word_tokenize(data[0]))
        train_set = [({feature: (feature in word_tokenize(data[0])) for feature in all_features}, data[1]) for data in data_set]
        # training
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        # get content
        sentence = content.lower()
        # tokenize words
        words = word_tokenize(sentence)
        # words stemming
        ps = PorterStemmer()
        # stop words
        stop_words = set(stopwords.words('english'))
        # filter words
        filtered_words = []
        for word in words:
            # filter out all stop words and punctuations
            if (word.isalpha()) and (word not in stop_words):
                filtered_words.append(ps.stem(word))
        # prediction
        test_features = {feature.lower(): (feature in filtered_words) for feature in all_features}
        result = classifier.classify(test_features)
        return result
