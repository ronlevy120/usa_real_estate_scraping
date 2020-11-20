import os
import urllib.request

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import argparse
import sqlite3
import os
import contextlib
import itertools
import random
from datetime import datetime
import csv

DB_FILENAME = 'usa_scraping_database.db'

def list_of_places():
    parser = argparse.ArgumentParser(description="scraper")
    parser.add_argument('places',
                        help="Places in the US to look for, space between each place")
    args = parser.parse_args()
    return list(map(lambda x:x.lower(),args.places.split(' ')))

def get_image(place, page, driver, inner_folder):
    """
    Downloading images from a given site.
    :param driver: The webdriver used in selenium
    :param inner_folder: the folder where the image is store, created by make_inner_folder()
    :place The location of the property. This is the parent folder
    :i Page number
    :return: None. That function is just downloading the images
    """
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    img_tags = soup.find_all('img')
    img_urls = [img['src'] for img in img_tags]
    for j, img in enumerate(img_urls):  # All images from that location
        extension = img.split('.')[-1][:3]
        if extension == 'net':
            extension = 'png'
        elif extension == 'jpe':
            extension = 'jpeg'
        file_name = f"img_{j}." + extension
        try:
            urllib.request.urlretrieve(img, os.path.join(place, page,  inner_folder, file_name))
        except ValueError:
            pass


def get_urls(driver):
    """
    Get all the url's in a specific web page.
    :param driver: The webdriver used in selenium
    :return: A list of all url's in that page
    """
    page_urls = driver.find_elements_by_css_selector(".tAddress [href]")
    urls = [cell.get_attribute('href') for cell in page_urls]  # All urls in that page
    return urls


def make_inner_folder(place, idx, cell_url, page):
    """
    Create a folder inside the appropriate place folder
    :param idx: The index of the url from the url's list
    :param cell_url: The cell in the table which we're working on
    :place The location of the property. This is the parent folder
    :page Page number
    :return: the name of the folder that has been just created
    """
    inner_folder = str(idx + 1) + '__' + cell_url[-15:]
    if not os.path.exists(os.path.join(place, page, inner_folder)):
        os.mkdir(os.path.join(place, page, inner_folder))
    return inner_folder


def info_data(driver):
    """
    Get the informative data regarding the propary
    :param driver: The webdriver used in selenium
    :return: list of table of relevant data
    """
    try:
        full_address = driver.find_element_by_class_name('fullAddress').text
    except NoSuchElementException:
        full_address = None
        pass
    try:
        just_listed_status = driver.find_element_by_class_name('justlisted').text
    except NoSuchElementException:
        just_listed_status = None
        pass
    try:
        reo_id = driver.find_element_by_class_name('reoid').text
    except NoSuchElementException:
        reo_id = None
        pass
    try:
        mls_id = driver.find_element_by_class_name('mlsid').text
    except NoSuchElementException:
        mls_id = None
        pass
    try:
        agent_name = driver.find_element_by_class_name('agent-name').text
    except NoSuchElementException:
        agent_name = None
        pass
    try:
        agent_phone = driver.find_element_by_class_name('_agent-phone').text
    except NoSuchElementException:
        agent_phone = None
        pass
    try:
        agent_company_name = driver.find_element_by_class_name('company-name').text
    except NoSuchElementException:
        agent_company_name = None
        pass
    try:
        agent_company_phone = driver.find_element_by_class_name('company-phone').text
    except NoSuchElementException:
        agent_company_phone = None
        pass
    try:
        agent_company_address = driver.find_element_by_class_name('company-address').text
    except NoSuchElementException:
        agent_company_address = None
        pass

    try:
        description = driver.find_element_by_class_name('class="description-body').text
    except NoSuchElementException:
        description = None
        pass
    return full_address, just_listed_status, reo_id, mls_id, agent_name, agent_phone, agent_company_name, \
           agent_company_phone, agent_company_address, description


def table_data(driver):
    """
    Get the data regarding the propary from all tables in that page
    :param driver: The webdriver used in selenium
    :return: List of tuples with the relevant data
    """
    table_values = [ele.text for ele in driver.find_elements_by_class_name('attr-value')]
    table_label = [ele.text for ele in driver.find_elements_by_class_name('attr-label')]
    zip_list = list(zip(table_label, table_values))
    return zip_list


def main():
    WEBDRIVER_PATH = r"C:\Users\user\Documents\the_webdriver\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=WEBDRIVER_PATH)  # You MUST install WebDriver first
    HOMEPAGE = "https://www.homepath.com/listings/"
    places = list_of_places()
    for place in places:
        if not os.path.exists(place):
            os.mkdir(place)
        url = HOMEPAGE + place + '/' + "list_v"
        driver.get(url)
        page = 1
        while len(driver.find_elements(By.TAG_NAME, "td")) > 3:
            if page > 1:
                url = HOMEPAGE + place + f"/{page}_p/list_v"
            driver.get(url)
            page = str(page)
            if not os.path.exists(os.path.join(place, page)):
                os.mkdir(os.path.join(place, page))
            urls = get_urls(driver)
            for idx, cell_url in enumerate(urls):
                print(f"Page number: {page}")
                inner_folder = make_inner_folder(place, idx, cell_url, page)
                print(f"Folder name:{inner_folder}")
                driver.get(cell_url)
                get_image(driver=driver, inner_folder=inner_folder, place=place, page=page)
                print(info_data(driver))
                print(table_data(driver))
            driver.get(url)
            print(f"End of loop {page}")
            page = int(page)
            page += 1

DB_FILENAME = 'usa_scraping.db'

def sql():
    with contextlib.closing(sqlite3.connect(DB_FILENAME)) as con:  # auto-closes
        with con:  # auto-commits
            cur = con.cursor()
            cur.execute('pragma foreign_keys')
            cur.execute("""INSERT OR IGNORE INTO agents (idagents, agent_name ,agent_phone, idproerties)
            VALUES (?, ?, ?, ?)""",[])
            cur.execute("""INSERT OR IGNORE INTO properties (
            idproperties ,address, just_list, reo_id, mls_id)
            VALUES (?, ?, ?, ?, ?)""",[])
            cur.execute("""INSERT OR IGNORE INTO company (
            idcompany, comp_name, comp_phone, comp_address, idproperties)
            VALUES (?, ?, ?, ?, ?)""",[])
            cur.execute("""INSERT OR IGNORE INTO prop_description (
            idprop_description, description, idproperties)
            VALUES (?, ?, ?)""",[])
            cur.execute("""INSERT OR IGNORE INTO images (
            idimages, img_name, folder, page, place, idproperties)
            VALUES (?, ?, ?, ?, ?, ?)""",[])
            cur.execute("""INSERT OR IGNORE INTO property_detailes (
            id_property_detailes, idproperties, price, bedrooms, Bathrooms, 
            `Full Baths`, `Garage Description`, `Basement`, `Total Rooms`, `Living Area Size`,
            `Lot Size in acres`, `Style`, `Exterior`, `Roof`, `Flooring`, 
            `Air Conditioning`, `Utilities`, `Pool`, `Sewer Type`, `HOA`, 
            `HOA Fees is US Dollar`, `Year Built`)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",[])
            cur.execute("""INSERT OR IGNORE INTO Property_Tax_Roll_Details (
            `idProperty Tax Roll Details`, `Elementary School`, 
            `Junior High School`, `Senior High School`,
            `Subdivision` , `idproperties`)
            VALUES (?, ?, ?, ?, ?, ?)""",[])
            cur.execute("""INSERT OR IGNORE INTO County_Tax_Roll_Details (
            `idCounty_Tax_Roll_Details`, `Air Conditioning`, 
            `Bedrooms`, `Fireplaces`, `Half Baths`, 
            `Property Type`, `APN`, `Baths`, `Construction Type`, `Full Baths`,
            `Land Area`, `Num_of Stories`, `idproperties`)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",[])
            con.commit()




if __name__ == '__main__':
    main()
