from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

#--| Setup
options = Options()
#options.add_argument("--headless")
options.add_argument("--incognito")
options.add_argument('--disable-extensions')
options.add_argument('--profile-directory=Default')
options.add_argument("--incognito")
options.add_argument("--disable-plugins-discovery");
options.add_argument("--start-maximized")
caps = webdriver.DesiredCapabilities().FIREFOX
#caps["marionette"] = True
browser = webdriver.Firefox(firefox_options=options)#, capabilities=caps)
browser.delete_all_cookies()
#wait = new WebDriverWait(browser, 30)
#--| Parse
browser.get('https://data.gov.il/dataset/covid-19/resource/8a21d39d-91e3-40db-aca1-f73f7ab1df69/view/58688c13-ad90-4e4c-98c6-e5ee53fe1b2f')
logo = browser.find_elements_by_css_selector('.data-view-container')
print(logo)
