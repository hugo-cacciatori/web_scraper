import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json
import csv
import os

#The main function. We give the program a search url from Doctolib, here it's every physiotherapist of the PACA region. It's going to collect the name, adress and phone number of every search result.
def scrape_doctolib():
    search_url = f"https://www.doctolib.fr/kinesitherapie-du-sport/provence-alpes-cote-d-azur?page=1"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    profile_urls = scrape_search_page(search_url, driver) #get the url of every profile
    for url in profile_urls:
        time.sleep(random.uniform(4.8, 6.5))
        scrape_profile(url, driver) #get the data from each profile
    driver.quit()

#Generates a sample.json file from a json object
def describe_json(json_data):
    with open("sample.json", "w") as outfile:
        json.dump(json_data, outfile)

#Formats a given phone number to a string in the french format (+33 in place of the zero)
def format_phone_number_fr(phone_number):
    if(phone_number != None):
        phone_number = str(phone_number)
        if(phone_number[0:3] != "+33"):
            return f'+33{phone_number[1:]}'.replace(" ", "")
        else:
            return phone_number
    return phone_number

#Uses Selenium to get the search page and collect the url of every search results
def scrape_search_page(search_url, driver):
    profile_urls = []
    button_attributes = []
    is_button_clickable = True
    driver.get(search_url)
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button#didomi-notice-agree-button>span"))).click() #Accept the cookie button
    while(is_button_clickable): #As long as we can click on "Suivant"
        time.sleep(1)
        profile_urls = profile_urls + [a.get_attribute('href') for a in driver.find_elements(By.XPATH, "//div[@class='dl-search-result-avatar']/a")]
        next_button = driver.find_element(By.XPATH, "//button[@class='Tappable-inactive dl-button-tertiary-primary next-link dl-button dl-button-size-medium']")
        button_attributes = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', next_button)
        for a in button_attributes: #check if the button is clickable
            if 'disabled' in a:
                print('button is disabled')
                is_button_clickable = False
                break
        if not is_button_clickable: break #Ensure that we exit the while loop if the condition is set to False 
        print('button is clickable')
        time.sleep(random.uniform(4.8, 6.5)) #We wait a random amount of time in between clicks to simulate a human user and to not overload the server.
        driver.execute_script("arguments[0].click();", next_button)
    print(f'{len(profile_urls)} urls collected !')
    return profile_urls

#Extracts the wanted data from a profile. The data is in a <ld+json> html tag, we convert that data to a python json object and we then store it into a .csv file.
def scrape_profile(url, driver):   
    driver.get(url)
    page = driver.page_source 
    soup = BeautifulSoup(page, "html.parser")
    p = soup.find('script', {'type':'application/ld+json'})
    json_data = json.loads("".join(p))
    # describe_json(json_data) #uncomment this line if you want to check the content of the json that is being extracted
    if json_data['@type'] == 'Physician': #this line ensures that the profile is from a physician and filters out the potential hospital profiles that could have a different data structure.
        filename = "kine_array.csv"
        column_headers = ['Nom', 'Rue', 'Code Postal', 'Ville', 'Telephone']
        row_data = [json_data['name'], json_data['address']['streetAddress'], json_data['address']['postalCode'], json_data['address']['addressLocality'], format_phone_number_fr(json_data['telephone'])]
        for e in row_data:
            print(e)
        if os.path.exists(filename): #if the csv file already exists, we append to it, else, we create it
            with open(filename, 'a',  encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(row_data)
        else: 
            with open(filename, 'w',  encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(column_headers)
                writer.writerow(row_data)

scrape_doctolib()