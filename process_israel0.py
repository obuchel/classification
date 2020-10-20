#nb-tree-grid ng-star-inserted

#https://stackoverflow.com/questions/2935658/beautifulsoup-get-the-contents-of-a-specific-table

import urllib.request as urllib2
#https://datadashboard.health.gov.il/COVID-19/general
#from urllib2 import urlopen, HTTPError
from bs4 import BeautifulSoup
import csv

#soup = BeautifulSoup (open("https://datadashboard.health.gov.il/COVID-19/general"), features="lxml")
url="https://datadashboard.health.gov.il/COVID-19/general"
html = urllib2.urlopen(url).read()
bs = BeautifulSoup(html)
#print(bs)
table = bs.find(lambda tag: tag.name=='ngx-app')# and tag.has_attr('id') and tag['id']=="Table1")
rows = table.findAll(lambda tag: tag.name=='tr') 
#rows = table.findAll(lambda tag: tag.name=='tr')
print(table)
