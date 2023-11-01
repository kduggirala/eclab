# CANNAPAGES DATA COLLECTION 

# IMPORTS
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time


#Reading in city data:
cities = pd.read_csv("most_pop_cities.csv", header = None).drop_duplicates()[0].apply(lambda s : s.replace(" ", "-"))

# SETUP WEBDRIVER
c = webdriver.ChromeOptions()
c.add_argument("--incognito")
driver = webdriver.Chrome(options = c)
#driver = webdriver.Chrome("C:/Users/dand2/Desktop/Chrome_Web_Driver/chromedriver-win64/chromedriver-win64/chromedriver.exe", options = c)
driver.maximize_window()

""" Current strategy """
base_url = "https://cannapages.com/listings/near/"
for city in cities:
    driver.get(base_url + city)
    time.sleep(0.25)
    soup = BeautifulSoup(driver.page_source, "lxml")
    stores = [(x.find("h3", {"slot":"title"}).find("a").text, x.find("div", {"class":"text-muted text-nowrap text-capitalize"}).text) 
          for x in soup.find_all("div", {"data-ms-index":"listings"})]

pd.DataFrame(stores).drop_duplicates().rename({0 : "Store Name", 1 : "Type"}, axis = 1).to_csv("cannapages.csv", index = False)