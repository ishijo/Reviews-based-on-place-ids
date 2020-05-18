######   https://search.google.com/local/reviews?placeid=ChIJI-_g-cDlDDkRRRf6NOBqV_E             
######   https://search.google.com/local/reviews?placeid=ChIJlSobTU_kDDkRvu2PW0G--4I
######    https://search.google.com/local/reviews?placeid=ChIJm-5b4FBIbDkRY7hOLUBnjRs
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

# chrome_options = Options()
# #chrome_options.add_argument("--lang=en")
# chrome_options.add_argument("--disable-extensions")
# browser = webdriver.Chrome(chrome_options=chrome_options)
cdpath='/Users/ishikajohari/Desktop/Projects/google-review-scrape/chromedriver'

## https://search.google.com/local/writereview?placeid=<place_id>
## https://maps.googleapis.com/maps/api/place/details/json?placeid={place_id}&key={api_key}
## ChIJlSobTU_kDDkRvu2PW0G--4I      -MOI
## ChIJI-_g-cDlDDkRRRf6NOBqV_E       -School
###### https://search.google.com/local/reviews?placeid=
    ## l-> https://search.google.com/local/reviews?placeid=ChIJW7aB9gX5DogRXcljbEdemXE


## https://www.google.com/maps/@28.567339,77.3189626,17z/data=!3m1!4b1


api_key = False
# If you have a Google Places API key, enter it here
# api_key = 'AIzaSy___IDByT70'

if api_key is False:
    api_key =
    serviceurl = ""
else :
    serviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


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

''') ### THINK ABOUT IT


###################################################
placeidlink="https://search.google.com/local/reviews?placeid="
count=0
while(True):
    if(count>5):
        print('Retrieved 5 locations, restart to retrieve more')
        break
    place=input('Enter Location:\n (To exit, Enter N)')
    if(place=='n'):
        break
    ### then should store all reviews in the database

    parms = dict()
    parms["address"] = place
    if api_key is not False: parms['key'] = api_key
    url = serviceurl + urllib.parse.urlencode(parms)   # SAME AS - http://py4e-data.dr-chuck.net/json?address=Mall+of+india+noida&key=42

    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx) ##
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

    #print(json.dumps(js, indent=4),end='\n\n')
    pid=js['results'][0]['place_id']
    #print("PLACE ID:  ",pid)

    cur.execute('''INSERT INTO Places (placeid, name)
            VALUES ( ?, ? )''', (memoryview(pid.encode()), memoryview(place.encode()) ) )
    # cur.execute('''INSERT INTO Reviews (placeid)
    #         VALUES ( ? )''', (memoryview(pid.encode()),)  )

    conn.commit() # most imp --> its important to be inside the loop to prevent loss of data with each loop cycle


    placeidurl=placeidlink+pid   # U R L here      <---------
    print('Opening url...')


    browser= webdriver.Chrome(cdpath)        ##TO OPEN IN A CHROME TAB
    browser.get(placeidurl)                        ## ''



    #################################
    wait = WebDriverWait(browser, 10)
    menu_bt = wait.until(EC.element_to_be_clickable(
                           (By.XPATH, '//g-dropdown-button[@class=\'dkSGpd NkCsjc\']'))
                       )
    menu_bt.click()
    # recent_rating_bt = browser.find_elements_by_xpath(
    #                                      '//g-menu[@role=\'menuitemradio\']')#zPXzie;;BRDJ7w     INITIAL

    # recent_rating_bt = browser.find_elements_by_xpath('//g-menu[@role=\'menuitemradio\']')
    # recent_rating_bt_2=recent_rating_bt.find_elements_by_xpath('//div[@class='znKVS' and .='Newest']')    #FIRST

    recent_rating_bt=browser.find_element_by_xpath("//g-menu[@role='menu']//div[@class='znKVS'][text()='Newest']")

    # recent_rating_bt_1=browser.find_elements_by_xpath('//g-menu')
    # recent_rating_bt = recent_rating_bt_1.find_elements_by_xpath('//g-menu-item[@role=\'menuitemradio\']')
    # recent_rating_bt_2=recent_rating_bt.find_elements_by_xpath('//div[@class='znKVS' and .='Newest']')       #SECOND



                                         #["//*[text()='Newest']"]
                                         # '//div[@role='menuitem' and .='text']' this one
                                         #'//g-menu[@role=\'menuitemradio\']'

    recent_rating_bt.click()
    time.sleep(5)
    #################################


    #bsurl=requests.get(placeidurl)

    #soupurl=urllib.request.urlopen(placeidurl)
    soup=BeautifulSoup(browser.page_source, "html.parser")

    rlist = soup.find_all('div',{'jscontroller': "dWcZn"})
    # rlist=soup.find_all('div',{"class": "WMbnJf gws-localreviews__google-review"})# whole orange box class="WMbnJf gws-localreviews__google-review <REVIEW ID GOES HERE>
    #class="WMbnJf gws-localreviews__google-review r-if173jOLKpxA"

    print('I REACHED HERE') ##

    print('rlist length: ', len(rlist)) ##
    print('\n','rlist type: ',type(rlist),'\n\n') ##

    for r in rlist:

        r1=r('div', {"class": "jxjCjc"})

        r2=r1[0].find('div', {"class": 'TSUbDb'})
        r4=r2.find('a')
        personname=r4.string

        r3=r1[0].find('div', {"class": 'Jtu6Td'})
        r5=r3.find('span')
        personreview=r5.text
        if(len(personreview)<1):
            personreview='-Review without comments-'#Blank Review

        r6=r1[0].find('div',{'class': 'PuaHbe'})
        personrating=r6.span['aria-label']

        cur.execute('''INSERT INTO Reviews (placeid, name, review, rating)
        VALUES ( ?, ?, ?, ? )''', (pid, personname, personreview, personrating) )
        conn.commit()
    print('Reviews for',place,'are stored in the database now.', end='\n\n')
cur.close()
