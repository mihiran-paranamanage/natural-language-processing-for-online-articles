import requests
import urllib.parse
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from .summarize import Summarizer
from .categorize import Categorizer
import re

class NewsReader:

    def __init__(self):
        pass

    def search_results(self, comp_name):
        '''
        input : company name which to be searched from news websites
        output : details (category, title, content, url) of articles for all the related serach results
        '''
        ignore_words = ['pvt', 'ltd', 'plc', '(', ')', '.']
        comp_name = re.sub(r'|'.join(map(re.escape, ignore_words)), '', comp_name.lower()).strip()
        articles = []
        # sundayobserver
        url = 'http://www.sundayobserver.lk/search/node/%s' % urllib.parse.quote(comp_name, safe='')
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all('li', attrs={'class':'search-result'})
        if results:
            for result in results:
                article_url = result.find('a').get('href')
                article_page = requests.get(article_url)
                article_soup = BeautifulSoup(article_page.content, 'html.parser')
                article_title = article_soup.find('h1', attrs={'id':'page-title'}).text.strip()
                if self.is_relative(article_title, comp_name):
                    # compare title with company name
                    article_content = article_soup.find('div', attrs={'class': 'field-type-text-with-summary'}).text.strip()
                    article = {"url":article_url, "title":article_title, "content":Summarizer().summarize(article_content, 4), "category":Categorizer().categorize(article_content)}
                    articles.append(article)
                else: continue
        # dailymirror
        page = requests.post('http://www.dailymirror.lk/dailymirror/search', data={'search_text': comp_name})
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all('div', attrs={'class':'left-box'})
        if results:
            for result in results:
                article_url = result.find('a').get('href')
                article_page = requests.get(article_url)
                article_soup = BeautifulSoup(article_page.content, 'html.parser')
                article_title = article_soup.find('h1', attrs={'class':'inner-hd'}).text.strip()
                if self.is_relative(article_title, comp_name):
                    # compare title with company name
                    article_content = article_soup.find('div', attrs={'class': 'inner-text'}).text.strip()
                    article = {"url":article_url, "title":article_title, "content":Summarizer().summarize(article_content, 4), "category":Categorizer().categorize(article_content)}
                    articles.append(article)
                else: continue
        # return articles
        return articles

    def is_relative(self, seq_1, seq_2):
        ratio = SequenceMatcher(None, seq_1.lower(), seq_2.lower()).ratio()
        return ratio >= 0.4
