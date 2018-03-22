from django.db import models

'''
models for work with databases
all news associated with a company name
so this table should have a one-to-many relationship
'''

class Company(models.Model):
    comp_id = models.CharField(max_length=20,null=True,default='0')
    comp_name = models.CharField(max_length=200,default='0')
    comp_symbol = models.CharField(max_length=20,null=True,default='0')
    comp_lastTradedTime = models.CharField(max_length=20,null=True,default='0')
    comp_price = models.CharField(max_length=20,null=True,default='0')
    comp_turnover = models.CharField(max_length=20,null=True,default='0')
    comp_sharevolume = models.CharField(max_length=20,null=True,default='0')
    comp_tradevolume = models.CharField(max_length=20,null=True,default='0')
    comp_change = models.CharField(max_length=20,null=True,default='0')
    comp_changePercentage = models.CharField(max_length=20,null=True,default='0')
	
    def __str__(self):
        return self.comp_name

class News(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    news_category = models.CharField(max_length=20,default='0')
    news_title = models.CharField(max_length=200,default='0')
    news_url = models.CharField(max_length=400,default='0')
    news_content = models.CharField(max_length=1000,default='0')

    def __str__(self):
        return self.news_title
	

