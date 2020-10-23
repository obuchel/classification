

from selenium import webdriver
#from selenium.webdriver.safari.options import Options
import time

from selenium import webdriver                    # Import module 
from selenium.webdriver.common.keys import Keys   # For keyboard keys 
import time                                       # Waiting function  
URL = 'https://shopping.thinkwithgoogle.com'      # Define URL 


browser = webdriver.Safari()                       # Create driver object means open the browser
browser.get("https://data.gov.il/dataset/covid-19/resource/8a21d39d-91e3-40db-aca1-f73f7ab1df69/view/58688c13-ad90-4e4c-98c6-e5ee53fe1b2f")
#browser.get(URL)
link = "https://data.gov.il/dataset/covid-19/resource/8a21d39d-91e3-40db-aca1-f73f7ab1df69/view/58688c13-ad90-4e4c-98c6-e5ee53fe1b2f"
'''
import urllib.request

with urllib.request.urlopen(link) as url:
    s = url.read()
    # I'm guessing this would output the html source code ?
    print(s)
'''
