##### GATHERING ALL STATE / CITY PAGE LINKS #####
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

c = webdriver.ChromeOptions()
c.add_argument("--incognito")
driver = webdriver.Chrome(options = c)
driver.maximize_window()


file = open(f'./all_names_urls.csv', 'w', newline = '')
file_writer = csv.writer(file, delimiter = ',', quoting = csv.QUOTE_MINIMAL)

driver.get("https://weedmaps.com/dispensaries/sunnyside-dispensary-river-north")
driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div[2]/button[1]').click() #click the "I am above 21" button

base_url = "https://weedmaps.com"
driver.get("https://weedmaps.com/dispensaries/in/united-states")
soup = BeautifulSoup(driver.page_source, "lxml")

# Gathering links for each state page 
state_links = [state.get("href") for state in soup.find_all("a", {"class":"RegionLink-sc-5ee853d5-2 jDlsHT"})]

# Gathering city links for each state, create dictionary with keys as state names, values as lists of city links 
for state in state_links:
    driver.get(base_url + state)
    soup = BeautifulSoup(driver.page_source, "lxml")
    state_name = state.replace("/dispensaries/in/united-states/", "")
    file_writer.writerows([[city.get("href")] for city in soup.find_all("a", {"class":"RegionLink-sc-5ee853d5-2 jDlsHT"})])
    file.flush()