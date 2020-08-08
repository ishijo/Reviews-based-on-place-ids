# Overview
 To store reviews and rating of a particular place by using its placeid in an sqlite database format.

## Tools used
- ##### [DB Browser for SQLite](https://sqlitebrowser.org/dl/)
- ##### [Google Places API](https://developers.google.com/places/web-service/overview)
- ##### [Chromedriver](https://chromedriver.chromium.org/downloads)
(Make sure to replace the chromeriver executable file with your version)
- ##### [Selenium](https://pypi.org/project/selenium/)
- ##### [Beautiful Soup library](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## Walkthrough
- Navigate to the Project directory and run the 'greview.py' from your Terminal.
```
python greview.py
```
- Mention the Location of your choice (be mindful of the typos!) when prompted as:\
[Example]
```
(To exit, Enter 'n')
Enter Location: Mall of India, Noida
```
- Provided you installed the appropriate chromedriver [version](https://chromedriver.chromium.org/downloads), a seperate chrome window should open as follows:

 ![Chrome Window](https://github.com/ishijo/Reviews-based-on-place-ids/blob/master/Extra/imgs/chromedriver_window.png)
- Scroll through as many reviews as required. (Scrolling is necessary for extraction)
- The 'greviewdb.sqlite' will store all the reviews and corresponding info.  

 ![Structure of Database]('../../google-review-scrape/Extra/imgs/database_structure.png')  
 ![Stored data reviews](../../google-review-scrape/Extra/imgs/stored_data.jpg)

Note: The sqlite file won't retain any reviews after the next run of the script. In order change this, edit (see 'greview.py'):
```
DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS places;
```
