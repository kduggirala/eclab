# CANNAPAGES DATA COLLECTION 

# IMPORTS
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import csv

# SETUP WEBDRIVER
c = webdriver.ChromeOptions()
c.add_argument("--incognito")
driver = webdriver.Chrome(options = c)
#driver = webdriver.Chrome("C:/Users/dand2/Desktop/Chrome_Web_Driver/chromedriver-win64/chromedriver-win64/chromedriver.exe", options = c)
driver.maximize_window()

""" Current strategy """
base_url = "https://cannapages.com/listings/near/united-states/illinois/chicago/?type=listings"
driver.get(base_url)
soup = BeautifulSoup(driver.page_source, "lxml")
stores = [(x.find("h3", {"slot":"title"}).find("a").text, x.find("div", {"class":"text-muted text-nowrap text-capitalize"}).text) 
          for x in soup.find_all("div", {"data-ms-index":"listings"})]
# stores is a list of tuples formatted as (store_name, category)


""" Alternative strategy (work in progress)"""
# SETUP OUTPUT DICTIONARY 
final_dict = {"dispensaries": [], # Dispensaries
              "doctors": [], # Doctors
              "smoke-shops": [], # Smoke+Shops
              "grow-stores": [], # Grow+Stores
              "cbd-hemp-stores": [], # CBD%2FHemp+Stores
              "kratom-herbal": [], # Kratom%2FHerbal+Shops
              "cbd-massage": [], # CBD+Massage
              "cannabis-education": [], # Cannabis+Education
              "lounges": [], # Lounges
              "vape-shops": []} # Vape+Shops

base_url = "https://cannapages.com/"
ext = "/near/united-states/illinois/chicago/?type=listings&mapView=true"

for cat in final_dict.keys:
    driver.get(base_url + cat + ext)
    soup = BeautifulSoup(driver.page_source, "lxml")
    name_lst = [x.find("a").text for x in soup.find_all("h3", {"slot":"title"})]
    final_dict[cat] = name_lst