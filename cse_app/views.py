from django.shortcuts import get_object_or_404, render
import requests
from .models import Company, News
from .sunobserv import NewsReader

def index(request):
    # url : cse/
    context = {'titles': [("-------- SECTOR -------","0"), ("HOTELS AND TRAVELS","21"), ("PLANTATIONS","7")]}
    return render(request, 'cse_app/index.html', context)

def sectors(request, val):
    # url : cse/sectors/7
    r = requests.post('https://www.cse.lk/api/listBySector', data = {'sectorId':val})
    Company.objects.all().delete()
    for comp in r.json()['reqIndustryBySectors']:
        c = Company(comp_id=comp['id'], comp_name=comp['name'], comp_symbol=comp['symbol'], comp_lastTradedTime=comp['lastTradedTime'], comp_price=comp['price'], comp_turnover=comp['turnover'], comp_sharevolume=comp['sharevolume'], comp_tradevolume=comp['tradevolume'], comp_change=comp['change'], comp_changePercentage=comp['changePercentage'])
        c.save()
    return render(request, 'table_body.html', {'company_list':Company.objects.all()})

def categories(request, comp_id, val):
    # url : cse/news/categories/256/award
    comp = get_object_or_404(Company, pk=comp_id)
    if val=="all": articles = [comp.news_set.filter(news_url__contains='sundayobserver'), comp.news_set.filter(news_url__contains='dailymirror')]
    else: articles = [comp.news_set.filter(news_category=val, news_url__contains='sundayobserver'), comp.news_set.filter(news_category=val, news_url__contains='dailymirror')]
    return render(request, 'article_body.html', {'articles':articles})

def news(request, comp_id):
    # url : cse/news/256
    comp = get_object_or_404(Company, pk=comp_id)
    comp.news_set.all().delete()
    for article in NewsReader().search_results(comp.comp_name):
        comp.news_set.create(news_category=article['category'], news_title=article['title'], news_url=article['url'], news_content=article['content'])
    context = {'categories': [("--------- ALL ---------","all"), ("AWARDS","awards"), ("EXPANTION","expansion"), ("FINANCING","financing"), ("PRODUCTION","production"), ("OTHERS","others")], 'comp':comp, 'articles':[comp.news_set.filter(news_url__contains='sundayobserver'), comp.news_set.filter(news_url__contains='dailymirror')]}
    return render(request, 'cse_app/news.html', context)
