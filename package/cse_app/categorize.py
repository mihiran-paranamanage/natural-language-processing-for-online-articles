from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import names
import operator

class Categorizer:

    def __init__(self):
        pass

    def word_feats(self, words):
        return dict([(word, True) for word in words])

    def categorize(self, content):
        '''
        input: content of a article
        output: category of the article
        '''
        # data preparation
        position_Arr = [ 'position', 'vision', 'mission', 'goal', 'objective', 'authority', 'capital' ]
        awards_Arr = [ 'award', 'win', 'won', 'ceremony', 'congratulation', 'congratulate', 'honour', 'evaluation', 'judge', 'gold', 'golden' 'silver', 'bronze', 'merit' ]
        expanision_Arr = [ 'expansion', 'new', 'branch' 'bureau', 'division', 'office', 'section', 'wing', 'franchise', 'amalgamation' ]
        financing_Arr = [ 'finance', 'investment', 'asset', 'contribution', 'acquisition', 'purchase', 'loan', 'share', 'grant', 'cost' ]
        production_Arr = [ 'production' ]
        quality_Arr = [ 'quality', 'certificate', 'certificate', 'improvement' ]
        merchandising_Arr = [ 'merchandising' ]
        csr_Arr = [ 'corporate', 'social', 'responsibility' ]
        # feature extraction
        position_features = [(self.word_feats(pos), 'position') for pos in position_Arr]
        awards_features = [(self.word_feats(awa), 'awards') for awa in awards_Arr]
        expanision_features = [(self.word_feats(exp), 'expanision') for exp in expanision_Arr]
        financing_features = [(self.word_feats(fin), 'financing') for fin in financing_Arr]
        production_features = [(self.word_feats(pro), 'production') for pro in production_Arr]
        quality_features = [(self.word_feats(qua), 'quality') for qua in quality_Arr]
        merchandising_features = [(self.word_feats(mer), 'merchandising') for mer in merchandising_Arr]
        csr_features = [(self.word_feats(csr), 'csr') for csr in csr_Arr]
        train_set = position_features + awards_features + expanision_features + financing_features + production_features + quality_features + merchandising_features + csr_features
        # training
        classifier = NaiveBayesClassifier.train(train_set)
        # get content
        sentence = content.lower()
        # tokenize words
        words = word_tokenize(sentence)
        # words stemming
        ps = PorterStemmer()
        # stop words
        stopWords = set(stopwords.words('english'))
        # filter words
        wordsFiltered = []
        for word in words:
            # filter out all stop words and punctuations
            if (word.isalpha()) and (word not in stopWords):
                wordsFiltered.append(ps.stem(word))
        # categorizing
        ''' initial values '''
        position = 0
        awards = 0
        expanision = 0
        financing = 0
        production = 0
        quality = 0
        merchandising = 0
        csr = 0
        # evaluation
        for word in wordsFiltered:
            # prediction
            result = classifier.classify( self.word_feats(word))
            ''' vote for categories from predicted result '''
            if result == 'position':
                position = position + 1
            elif result == 'awards':
                awards = awards + 1
            elif result == 'expanision':
                expanision = expanision + 1
            elif result == 'financing':
                financing = financing + 1
            elif result == 'production':
                production = production + 1
            elif result == 'quality':
                quality = quality + 1
            elif result == 'merchandising':
                merchandising = merchandising + 1
            elif result == 'csr':
                csr = csr + 1
        lenth = len(wordsFiltered)
        ''' get results as a probability '''
        results = {"position":float(position)/lenth, "awards":float(awards)/lenth, "expanision":float(expanision)/lenth, "financing":float(financing)/lenth, "production":float(production)/lenth, "quality":float(quality)/lenth, "merchandising":float(merchandising)/lenth, "csr":float(csr)/lenth}
        ''' return the category that have a maximum probability '''
        return max(results.items(), key=operator.itemgetter(1))[0]
