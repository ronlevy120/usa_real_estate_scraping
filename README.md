# USA Real estate scraping
## Inbal Agur & Ron Levy & Ohad Hayoun



# Motivation
Real estate data can be powerful way to make smart decisions in both international and domestic market. 
This script allows you to achieve huge amount of data very easily.

# Table of Content
* [General info](#general-info)
* [Required files](#required files)
* [Installation](#Installation) 
* [How to use](#How to use)
* [Launch](#Launch)
* [Database](#Database)
* [ERD](#ERD)
* [Information and support](#information and support)

#General info
Scraping real estate data from USA government agencies has never been more easy.\
the data is taken from the following site: https://www.homepath.com/

#Required files
* main.py
* manager.py
* save_to_database.py
* create_database.py
* scraper.py
* stocks_api.py
* myconstants.py 
* ArgParseInput.py
* requirements.txt
* README.md
* .gitignore
* chromedriver.exe (instructions below)


# Installation

### requirements
To run this code, please install: 
- `Python` 3.x.
- `Chrome 'webdriver'` (available at: [https://chromedriver.chromium.org/downloads]("https://chromedriver.chromium.org/downloads"))
- `mysql`  (you may follow the instructions at:
https://www.youtube.com/watch?v=E0s9YlFHiO4&t=1s 



### packages list
Please make sure you have the following packages installed:
* beautifulsoup4==4.9.3
* configparser==5.0.0
* grequests==0.6.0
* matplotlib==3.3.3
* mysql-connector-python==8.0.22
* numpy==1.19.3
* pandas==1.1.3
* pandas-datareader==0.9.0
* pandas-finance==0.1.2
* preprocessing==0.1.13
* pycparser==2.20
* pyparsing==2.4.7
* requests==2.24.0
* scipy==1.5.4
* seaborn==0.11.0
* selenium==3.141.0
* SQLAlchemy==1.3.20
* tqdm==4.52.0
* urllib3==1.25.11


# How to use
### Pre-Launch
* edit the 'myconstants.py' file:
(crate a new file or use the file from the repository)

complete the constants values as follows:
- `HOMEPAGE` = "https://www.homepath.com/listings/"
- `LAST_ELEMENT` = -1
- `FULL_EXTENSTION` = 3
- `HALF_URL` = -15
- `DB_FILENAME` = the database file name (default = 'usa_scraping_database')

* Create a new file - 'passw.py':
this file should contain your personal info as follows:
- `DB_PATH` = the database file full path 'C:\...'
- `WEBDRIVER_PATH` = the webdriver file full path (example = "C:\Users\'user'\Documents\the_webdriver\chromedriver.exe")
- `HOST` = your 'mySQL' host name. (default = 'localhost')
- `USER` = your 'mySQL' user name. (default = 'root')
- `PASS` = your 'mySQL' password.

### Launch
Run the program from the main.py file. 

optional arguments for the main program:\

usage: main.py [-h] [places] [limit] [years]

arguments description:
* -h : arguments ```help``` description
* places : ```places``` in the US (city or states) to look for,with space between each place.
(Default: new-york)
* limit : limit the number of pages of houses scraping results (~40 houses per page) for the specific location.
* years : presents the US real estate main stocks performance chart for the last N years.\
          - [VGSIX] - Vanguard Real Estate Index Fund Investor Shares\
          - [FSRNX] - Fidelity Real Estate Index Fund\
          - [IYR] - iShares U.S. Real Estate ETF\

usage example: 'main.py los-angeles 25 10'

* this will execute scraping houses data in `Los Angeles`, 
presenting the `25` results pages, 
plotting the US real estate main stocks performance chart for the last `10` years
 
 
# Database
The database is made of the following tables:
* _agents_ - Real-estates agents who sale the properties in the databse
_* company_ - The companies where the real-estate agents works
* _county_tax_roll_details_ - County details about the properties
* _prop_description'_ - Description about the property
* _properties_ - a table of all properties. This table auto increment id is a foreign key for al tables
* _property_detailes_ - Morre details about the propery
* _property_tax_roll_details_ - Tax details about the property

# ERD
![ERD of the database](ERD.png)


# Information and support:
for more information and support please contact us by email:
[ronlevy12000@gmail.com](ronlevy12000@gmail.com) , [ohadohad5@gmail.com](ohadohad5@gmail.com) 