import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import ssl
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
from time import sleep

cdpath='/Users/ishikajohari/Desktop/Projects/google-review-scrape/chromedriver'

api_key = # Your API Key goes here
## (Of the form -> 'AIzaSy___IDByT70')

if api_key is False: # Ignore (Was relevant while writing the code.)
    api_key = #hidden
    serviceurl = #hidden
else :
    serviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

## Connecting to SQLite and creating tables while deleting existing info. (from previous runs of this code)
###################################################
conn = sqlite3.connect('greviewdb.sqlite')
cur = conn.cursor()
cur.executescript('''
DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS places;


CREATE TABLE Reviews (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    placeid TEXT,
    name    TEXT,
    review TEXT,
    rating TEXT
);

CREATE TABLE Places (
    placeid  TEXT NOT NULL PRIMARY KEY,
    name    TEXT
);

''')
###################################################

## Will be used later.  (Link to reach the google reviews for the specific place we take as input via the Place-ID)
placeidlink="https://search.google.com/local/reviews?placeid="

count=0

while(True):
    if(count>5):
        print('Retrieved 5 locations, restart to retrieve more')
        break
    ## Taking the place input from the user for which the reviews are to be founded
    place=input("(To exit, Enter 'n')\nEnter Location: ")
    if(place=='n'):
        break

    parms = dict()
    parms["address"] = place
    if api_key is not False: parms['key'] = api_key

    ## Of the form -> https://maps.googleapis.com/maps/api/place/details/json?placeid={place_id}&key={api_key}
    url = serviceurl + urllib.parse.urlencode(parms)

    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)

    ## Storing retrieved place information in JSON file (in order to extract PlaceID later)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters')
    count+=1

    try:
        js = json.loads(data)
    except:
        js = None

    if not js or 'status' not in js or js['status'] != 'OK':
        print('==== Failure To Retrieve ====')
        print(data)
        continue

    ## To extract the Place-ID (stored in 'pid' here) of the input Place from the JSON file
    pid=js['results'][0]['place_id']

    ## Store the corresponding retrieved information.
    cur.execute('''INSERT INTO Places (placeid, name)
            VALUES ( ?, ? )''', (memoryview(pid.encode()), memoryview(place.encode()) ) )

    conn.commit() ## Most imp --> its important for this to be inside the loop to prevent loss of data with each loop cycle.

    placeidurl=placeidlink+pid   # U R L here      <---------
    print('Opening url...')

    browser= webdriver.Chrome(cdpath)        ##TO OPEN IN A CHROME TAB
    browser.get(placeidurl)

    ## Using Selenium and Chromedriver to extract the specific review category to scrape
    #################################
    wait = WebDriverWait(browser, 10)
    menu_bt = wait.until(EC.element_to_be_clickable((By.XPATH, '//g-dropdown-button[@class=\'dkSGpd NkCsjc\']')))

    menu_bt.click()

    recent_rating_bt=browser.find_element_by_xpath("//g-menu[@role='menu']//div[@class='znKVS'][text()='Newest']")

    recent_rating_bt.click()
    time.sleep(5)
    #################################

    ## Parsing and storing text using the Beautiful Soup library
    soup=BeautifulSoup(browser.page_source, "html.parser")

    rlist = soup.find_all('div',{'jscontroller': "e6Mltc"})# earlier - dWcZn

    for r in rlist:

        r1=r('div', {"class": "jxjCjc"}) ## Corresponds to a particular customer review

        r2=r1[0].find('div', {"class": 'TSUbDb'}) ## Name
        r4=r2.find('a')
        personname=r4.string

        r3=r1[0].find('div', {"class": 'Jtu6Td'}) ## Review text
        r5=r3.find('span')
        personreview=r5.text
        if(len(personreview)<1):
            personreview='-Review without comments-' ## Blank Review

        r6=r1[0].find('div',{'class': 'PuaHbe'}) ## Rating Stars
        personrating=r6.span['aria-label']

        cur.execute('''INSERT INTO Reviews (placeid, name, review, rating)
        VALUES ( ?, ?, ?, ? )''', (pid, personname, personreview, personrating) )
        conn.commit()
    print('Reviews for',place,'are stored in the database now.', end='\n\n')
cur.close()
