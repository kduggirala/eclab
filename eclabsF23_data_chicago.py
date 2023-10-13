# DATA COLLECTION FROM WEEDMAPS (CHICAGO)

"""
VARIABLES WE NEED FOR EACH BUSINESS:
Name
Review Count
Average Reviews
License Information (may have multiple licenses for medical and recreational use)
Address
Phone?
Medical and recreational indicator variables
"""

"""
INFORMATION WE NEED FOR EACH PRODUCT SOLD BY EACH BUSINESS
Name (name may also contain quantity in grams or count)
Price (ideally per gram)
THC content
"""

# IMPORTS
import regex as re #regex might turn out to be useful so i'll keep it around
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import csv

def extract_data1(driver): #this should get the review count, name, average review rating, whatever else is immediately relevant on the store's opening page
    soup = BeautifulSoup(driver.page_source, 'lxml')
    Store_Name = soup.find("h1").get_text() # would be surprised if there were errors here, but maybe add error checking later?
    
    rating_wrapper = soup.find("div", class_ = "RatingWrapper-sc-6cf8fc1f-0 kxYFiI")
    Review_Counter = rating_wrapper.find("button")

    # If reviews exist, the button will have 5 elements under contents, and the review count will be the third. In this case, the average rating will be under a div
    # Otherwise, reviews don't exist and so we can just set Num_Reviews to 0 amd Avg_Rating to None
    try: 
        Num_Reviews = Review_Counter.contents[2]
        Avg_Rating = rating_wrapper.find("div").get_text()
    except (AttributeError, IndexError):
        Num_Reviews = 0
        Avg_Rating = None
        

    #banner includes stuff like is it recreational or medical, delivery or pickup, etc.
    banner_items = soup.find("div", class_ = "ChipWrapper-sc-b686745d-0 dcyYkr").find_all("div")
    descriptors = " | ".join(map(lambda e : e.get_text(), banner_items))

    phone = soup.find("a", {"aria-label" : "phone"})
    if phone:
        phone_number = phone.contents[1]
    else:
        phone_number = ""

    final = [Store_Name, Num_Reviews, Avg_Rating, descriptors, phone_number]


    final = [Store_Name, Num_Reviews, Avg_Rating, descriptors, phone]
    
    return final

def extract_data3(driver): #this should scrape the store details, including address, phone number, license info, etc.
    soup = BeautifulSoup(driver.page_source, 'lxml')
    licenses = " | ".join(map(lambda e : e.get_text(), soup.find_all("div", class_ = 'Text-sc-51fcf911-0 blMBuQ')))
    address = soup.find("div", {"data-testid" : "listing-address"}).get_text()
    return [licenses, address]

c = webdriver.ChromeOptions()
c.add_argument("--incognito")
driver = webdriver.Chrome(options = c)
driver.maximize_window()

fields = ["Name", "Number Reviews", "Avg Rating", "Descriptors", "Phone Number", "Licenses", "Address" "Url"]
file = open(f'./chicago_stores_data.csv', 'w', newline = '')
file_writer = csv.writer(file, delimiter = ',', quoting = csv.QUOTE_MINIMAL)
file_writer.writerow(fields)

driver.get("https://weedmaps.com/dispensaries/sunnyside-dispensary-river-north")
driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div[2]/button[1]').click() #click the "I am above 21" button

i = 1
while True:
    driver.get(f"https://weedmaps.com/dispensaries/in/united-states/illinois/chicago?page={i}")
    time.sleep(2)
    list = driver.find_element(By.XPATH, '//*[@data-testid="map-listings-list-wrapper"]')
    stores_list = list.find_elements(By.XPATH, './li')
    if len(stores_list) == 0: #if there's no stores listed on the page then we've gone past all the pages of data and can finish the loop
        break
    stores_links = [x.find_element(By.XPATH, "./div[1]/div[1]/div[1]/div/div[2]/a").get_attribute("href") for x in stores_list]
    for link in stores_links:
        driver.get(link)
        data = extract_data1(driver)

        driver.find_element(By.XPATH, '//button[@aria-label="store-details"]').click() #click store details button
        time.sleep(1) #wait for everything to load properly
        try:
            driver.find_element(By.XPATH, '//*[@id="details"]/div/div[1]/div/span/div/button').click() #click license info button
        except NoSuchElementException:
            pass
        data = data + extract_data3(driver) + [link]
        file_writer.writerow(data)
        file.flush()
    i += 1