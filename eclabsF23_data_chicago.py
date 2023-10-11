# DATA COLLECTION FROM WEEDMAPS (CHICAGO)

"""
High Level Pseudocode:
0) load the site (chicago, il dispensaries)
1) on each page (list of <= 30 stores):
    1.1) on each list element on the page (get the number of list elements on this page
        1.1.1) Click on a dispensary entry in list
            1.1.1.1) Store the following variables: business name, review count, average reviews
        1.1.2) On each page of products (click through with the next page button):
            1.1.2.1) Use BS to get the product info
        1.1.3) Click on store details: get the stuff from there (BeautifulSoup)
            1.1.3.1) remember to click the button for license info
        1.1.4) Remember to get any other relevant info on the site (reviews, store name, etc)
        1.1.5) click back/exit the store page
"""

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


c = webdriver.ChromeOptions()
c.add_argument("--incognito")
driver = webdriver.Chrome(options = c)
driver.maximize_window()

 
def extract_data1(): #this should get the review count, name, average review rating, whatever else is immediately relevant on the store's opening page
    #do some beautiful soup stuff here
    pass

def extract_data2(): #this should scrape the product info on this page
    #more beautiful soup, but this should be the most complicated one since this will involve checking for what kind of info is even available to begin with
    pass

def extract_data3(): #this should scrape the store details, including address, phone number, license info, etc.
    #more beautiful soup
    pass



driver.get("https://weedmaps.com/dispensaries/sunnyside-dispensary-river-north")
driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div[2]/button[1]').click() #click the "I am above 21" button

i = 1
while True:
    driver.get(f"https://weedmaps.com/dispensaries/in/united-states/illinois/chicago?page={i}")
    list = driver.find_element(By.XPATH, '//*[@data-testid="map-listings-list-wrapper"]')
    stores_list = list.find_elements(By.XPATH, './li')
    if len(stores_list) == 0: #if there's no stores listed on the page then we've gone past all the pages of data and can finish the loop
        break
    stores_links = [x.find_element(By.XPATH, "./div[1]/div[1]/div[1]/div/div[2]/a").get_attribute("href") for x in stores_list]
    for link in stores_links:
        driver.get(link)
        extract_data1()
        j = 1
        while True:
            driver.get(f"https://weedmaps.com/dispensaries/sunnyside-dispensary-river-north?page={j}")
            try:
                products_list = driver.find_element(By.XPATH, "//ol")
                extract_data2()
            except NoSuchElementException:
                break
            
            j += 1


        driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[3]/div/div[2]/button').click() #click store details button
        time.sleep(1) #wait for everything to load properly
        driver.find_element(By.XPATH, '//*[@id="details"]/div/div[1]/div/span/div/button').click() #click license info button
        extract_data3()

    i += 1





# SOME THINGS TO NOTE:
"""
1) Pages for each state and city seem simple to cycle through with string for-loops, e.g. dispensaries in chicago, 
illinois is just https://weedmaps.com/dispensaries/in/united-states/illinois/chicago

2) For each city/state page, you have to go through a few sub-pages of dispensaries to access all of them. Again we
can just loop through these, sub-page links all have the same structure. E.g. link for sub-page 4 of chicago dispensaries
is just https://weedmaps.com/dispensaries/in/united-states/illinois/chicago?page=4 
"""

# XPATHS
"""
1.1.1) XPATHS FOR DISPENSARY PAGE LINKS, 1st in list: 
//*[@id="content"]/div/div[2]/div[1]/div/div[2]/div[3]/div/ul/li[1]/div/div/div/div/div[2]/a

2nd in list
//*[@id="content"]/div/div[2]/div[1]/div/div[2]/div[3]/div/ul/li[2]/div[1]/div/div/div/div[2]/a (NOTE: where is div[1] coming from??)

3rd in list
//*[@id="content"]/div/div[2]/div[1]/div/div[2]/div[3]/div/ul/li[3]/div/div/div/div/div[2]/a

4th in list
//*[@id="content"]/div/div[2]/div[1]/div/div[2]/div[3]/div/ul/li[4]/div/div/div/div/div[2]/a
"""

"""
1.1.3) STORE DETAILS LINK XPATHS, 1st in list (access using click() function?):
//*[@id="content"]/div[2]/div[3]/div/div[2]/button

2nd in list:
//*[@id="content"]/div[2]/div[3]/div/div[2]/button

3rd in list:
//*[@id="content"]/div[2]/div[3]/div/div[2]/button

Looks like they are the same across different store pages (hopefully)
"""

"""
1.1.3.1) LICENSE INFO BUTTON, 1st in list:
//*[@id="details"]/div/div[1]/div/span/div/button

2nd in list:
//*[@id="details"]/div/div[1]/div/span/div/button

After clicking button, access license info using xpaths like these:

1st in list:
//*[@id="radix-:r1p:"]/div/div

2nd in list:
//*[@id="radix-:rq:"]/div/div

3rd in list:
//*[@id="radix-:rq:"]/div/div

Looks they are the same across store pages as well. 
"""
# BEAUTIFUL SOUP TO ACCESS BUSINESS VARIABLES (Before Store details button click):
"""
Name:

Review Count:

Average Reviews: 

"""
# BEAUTIFUL SOUP TO ACCESS BUSINESS VARIABLES (After Store details button click):
"""
License Information:

Address:

Phone?:

Medical and Recreational Indicator Variables:

"""
# BEAUTIFUL SOUP TO ACCESS PRODUCT VARIABLES FOR EACH BUSINESS:
"""
Name:

Price (ideally per gram):

THC Content:

"""