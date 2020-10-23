import os
import re
import time
from typing import Optional
import pandas as pd
#import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import webbrowser
import requests
res = requests.get('https://automatetheboringstuff.com/files/rj.txt')
type(res)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


#from selenium.webdriver.support.expected_conditions import presence_of_element_located
#import controller
#URL = 'https://public.tableau.com/profile/fabio.baraghini#!/vizhome/CuebiqMobilityIndexAnalysis/MobilityIndexMarketArea'
#URL='https://public.tableau.com/profile/fabio.baraghini#!/vizhome/CuebiqMobilityIndexAnalysis/CBSAMobilityIndex'
URL0 = 'https://e.data.gov.il/dataset/f54e79b2-3e6b-4b65-a857-f93e47997d9c/resource/8a21d39d-91e3-40db-aca1-f73f7ab1df69/download/corona_city_table_ver_003.csv'

#res = pd.read_csv(URL0)
#print(res)
#URL = 'https://data.gov.il/dataset/covid-19/resource/8a21d39d-91e3-40db-aca1-f73f7ab1df69'
URL = 'http://data.gov.il/dataset/covid-19/resource/8a21d39d-91e3-40db-aca1-f73f7ab1df69/view/58688c13-ad90-4e4c-98c6-e5ee53fe1b2f'
#URL2="http://cnn.com"

'''
op=webbrowser.open_new(URL)
import pandas as pd
import numpy as np
import requests as rq
from bs4 import BeautifulSoup 

pg = rq.get(op)
soup = BeautifulSoup(pg.content, 'lxml')
table = soup.findAll("div", {"class": "data-view-container"})
print(table)
'''





#webbrowser.get(using=None)
#controller.open(ULR, new=0, autoraise=True)
def set_up_driver():
    chrome_options = Options()
    userProfile= "/Users/olgabuchel/";
    #chrome_options.add_argument("--incognito")
    '''
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-plugins-discovery")
    '''
    
    #chrome_options.add_argument("user-data-dir="+userProfile)
    #chrome_options.add_argument("user-data-dir=/Users/olgabuchel/Downloads/DeckSample/classification_project")
    driver = webdriver.Chrome(chrome_options=chrome_options,executable_path='/Users/olgabuchel/myAnaconda/mobility/chromedriver')
    
    #driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
    #driver.manage().window().maximize();
    #print(driver)
    #options = new ChromeOptions();
    #driver = webdriver.Chrome(executable_path='/Users/olgabuchel/myAnaconda/mobility/chromedriver')
    #driver.get(URL)
    driver.get(URL)
    #driver.navigate().to(URL)
    
    WebDriverWait(driver, 25).until(
        EC.presence_of_element_located((By.XPATH, "//*[@class='data-view-container']"))
    )
    
    #print(driver)
    #Wait to load
    time.sleep(20)

     # Switch to the embedded tableau iframe
    #iframe = driver.find_element_by_class_name('data-view-container')
    #driver.switch_to.frame(iframe)

    return driver


def scrape_week(
    driver: Optional[webdriver.Chrome] = None,
    close_driver: bool = False,
    ) -> str:
    if driver is None:
        driver = set_up_driver()

    week_div = driver.find_element_by_xpath("//div[@class='data-view-container']")
    week_text = week_div.text
    formatted_week = week_text.lower().replace(' ', '__').replace('-', '')
    #print(formatted_week)
    '''
    scroll = driver.find_element_by_xpath(
      "//div[@class='tab-tvScrollY tvimages'][./div[@class='tvimagesContainer' and @style]]"
    )
    # column = driver.find_elements_by_xpath("//canvas[@class='tabCanvas tab-widget']")[1]

    # Reset the scroll bar to the top just in case
    driver.execute_script('arguments[0].scrollTop = (0,0)', scroll)

    # Scroll down in increments
    for i in range(1, 95):
        driver.execute_script('arguments[0].scrollTop = (0,%s)' % str(i * 400), scroll)
        time.sleep(1.0)

    data_containers = []
    # Looking for the tvimagesContainer objects with the highest number of images as children
    # There should only be two with large values, corresponding to the two data column types.
    for x in driver.find_elements_by_class_name('tab-clip'):
        print(x)
        for y in x.find_elements_by_class_name('tvimagesContainer'):
            print(y)
            if len(y.find_elements_by_tag_name('img')) > 20:
                data_containers.append(y)
    print(data_containers)
    assert len(data_containers) == 2

    # Figure out which container has locations and which has data
    container_1_src = data_containers[0].find_element_by_tag_name('img').get_attribute('src')

    def get_sources(container):
        return [img.get_attribute('src') for img in container.find_elements_by_tag_name('img')]

    if 'yheader.0.0' in container_1_src:
        headers = get_sources(data_containers[0])
        values = get_sources(data_containers[1])
    else:
        headers = get_sources(data_containers[1])
        values = get_sources(data_containers[0])

    # Make directories if they do not exist
    if not os.path.isdir(formatted_week):
        os.mkdir(formatted_week)
    header_dir = os.path.join(formatted_week, 'headers')
    value_dir = os.path.join(formatted_week, 'values')
    for dirname in [header_dir, value_dir]:
        if not os.path.isdir(dirname):
            os.mkdir(dirname)

    # Gather the img children from each data container and download all of 'em
    for idx, src_url in enumerate(headers):
        header_pattern = '(yheader\.\d+\.\d+.png)'
        save_filename = re.search(header_pattern, src_url).groups()[0]
        savename = os.path.join(header_dir, save_filename)

        img_data = requests.get(src_url).content
        with open(savename, 'wb') as file:
            file.write(img_data)

        print(f'Saved {idx + 1} / {len(headers)} headers')

    for idx, val_url in enumerate(values):
        value_pattern = '(viz\.\d+\.\d+.png)'
        save_filename = re.search(value_pattern, val_url).groups()[0]
        savename = os.path.join(value_dir, save_filename)

        img_data = requests.get(val_url).content
        with open(savename, 'wb') as file:
            file.write(img_data)

        print(f'Saved {idx + 1} / {len(headers)} values')

    if close_driver:
        driver.close()

    # Return the dirname where the week data was saved
    return formatted_week
    '''

if __name__ == '__main__':
    scrape_week(close_driver=True)
