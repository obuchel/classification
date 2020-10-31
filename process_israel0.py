#curl -d '%7B%22resource_id%22%3A%228a21d39d-91e3-40db-aca1-f73f7ab1df69%22%2C%22q%22%3A%22%22%2C%22filters%22%3A%7B%7D%2C%22include_total%22%3Atrue%2C%22limit%22%3A62601%2C%22offset%22%3A0%7D' https://data.gov.il/api/3/action/datastore_search -o israel_data_today.json


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
bs = BeautifulSoup(html,features="html.parser")
#print(bs)
table = bs.find(lambda tag: tag.name=='ngx-app')# and tag.has_attr('id') and tag['id']=="Table1")
rows = table.findAll(lambda tag: tag.name=='table') 
#rows = table.findAll(lambda tag: tag.name=='tr')
print(table)
