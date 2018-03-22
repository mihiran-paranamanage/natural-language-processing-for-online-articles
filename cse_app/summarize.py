from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from heapq import nlargest

class Summarizer:
    
    def __init__(self):
        self.min_cut = 0.1
        self.max_cut = 0.9

    def compute_frequencies(self, words_sentences):
        '''
        returns a dictionary which includes frequencies for all filtered words
        freq_dict_[word] gives a frequency of the word
        '''
        stopWords = set(stopwords.words('english'))
        freq_dict = defaultdict(int)
        for words in words_sentences:
            for word in words:
                # filter out all stop words and punctuations
                if (word.isalpha()) and (word not in stopWords):
                    freq_dict[word] += 1
        max_val = float(max(freq_dict.values()))
        freq_dict_ = defaultdict(int)
        for word in freq_dict.keys():
            word_freq = freq_dict[word]/max_val
            if not (self.min_cut < word_freq < self.max_cut):
                freq_dict_[word] = word_freq
        return freq_dict_

    def summarize(self, content, n):
        '''
        input: content of a article, number of sentences should have
        output: summarized text of the article
        '''
        sentences = sent_tokenize(content)
        words_sentences = [word_tokenize(sentence.lower()) for sentence in sentences]
        freq_dict = self.compute_frequencies(words_sentences)
        rank_dict = defaultdict(int)
        for i,words in enumerate(words_sentences):
            for word in words:
                if word in freq_dict:
                    rank_dict[i] += freq_dict[word]
        ranked_ids = self.rank(rank_dict, n)
        results = [sentences[ranked_id] for ranked_id in ranked_ids]
        ordered_result = self.reorder_sentences(results, content)
        return ' '.join(ordered_result)

    def rank(self, rank_dict, n):
        return nlargest(n, rank_dict, key=rank_dict.get)

    def reorder_sentences(self, results, content):
        results.sort(key = lambda x: content.find(x))
        return results
        
