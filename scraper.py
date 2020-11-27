import os
import urllib.request
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from myconstants import *
from passw import *


class Scraper:

    def __init__(self, place, path_to_driver):
        """Initialize Scraper class. Define place and path to the web driver"""
        self.place = place
        self.path_to_driver = path_to_driver

    def create_driver(self):
        """Creates a driver with the path initialized at the init method"""
        self.driver = webdriver.Chrome(executable_path=self.path_to_driver)

    def get_image(self, page, inner_folder):
        """
        Downloading images from a given site.
        :param inner_folder the folder where the image is store, created by make_inner_folder()
        :page the current page in the site the scraper is working on
        :return: None. That function is just downloading the images
        """
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        img_tags = soup.find_all('img')
        img_urls = [img['src'] for img in img_tags]
        for j, img in enumerate(img_urls):  # All images from that location
            extension = img.split('.')[LAST_ELEMENT][:FULL_EXTENSTION]
            if extension == 'net':
                extension = 'png'
            elif extension == 'jpe':
                extension = 'jpeg'
            file_name = f"img_{j}." + extension
            try:
                urllib.request.urlretrieve(img, os.path.join(self.place, page, inner_folder, file_name))
            except ValueError:
                pass

    def tables_len(self):
        """return the len of a Selenium object"""
        return len(self.driver.find_elements(By.TAG_NAME, "td"))

    def driver_get(self, url):
        """Update the driver to the received url"""
        self.driver.get(url)

    def get_urls(self):
        """
        Get all the url's in a specific web page.
        :return: A list of all urls in that page
        """
        page_urls = self.driver.find_elements_by_css_selector(".tAddress [href]")
        urls = [cell.get_attribute('href') for cell in page_urls]  # All urls in that page
        return urls

    def make_inner_folder(self, idx, cell_url, page):
        """
        Create a folder inside the appropriate place folder
        :param idx: The index of the url from the url's list
        :param cell_url: The cell in the table which we're working on
        :page the current page in the site the scraper is working on
        :return: the name of the folder that has been just created
        """
        inner_folder = str(idx + 1) + '__' + cell_url[HALF_URL:]
        if not os.path.exists(os.path.join(self.place, page, inner_folder)):
            os.mkdir(os.path.join(self.place, page, inner_folder))
        return inner_folder

    def full_address(self):
        """Return the house owner full address. Converting Selenium object to text"""
        try:
            return self.driver.find_element_by_class_name('fullAddress').text
        except NoSuchElementException:
            return

    def just_listed_status(self):
        """
        the status of the listed house - weather it's just list or not.
        return True if it just listed, False otherwise
        """
        try:
            if self.driver.find_element_by_class_name('justlisted').text == "Status: Just Listed":
                return True
            else:
                return False
        except NoSuchElementException:
            return

    def reo_id(self):
        """return the reo_id of the property as a string"""
        try:
            return self.driver.find_element_by_class_name('reoid').text.split(':')[1]
        except NoSuchElementException:
            return

    def mls_id(self):
        """return the mls_id of the property as a string"""
        try:
            return self.driver.find_element_by_class_name('mlsid').text.split(':')[1]
        except NoSuchElementException:
            return

    def agent_name(self):
        """return string of the name of the real-estate agent who's selling the house"""
        try:
            return self.driver.find_element_by_class_name('agent-name').text
        except NoSuchElementException:
            return

    def agent_phone(self):
        """return string of the phone number of the real-estate agent who's selling the house"""
        try:
            return self.driver.find_element_by_class_name('_agent-phone').text.split(':')[1]
        except NoSuchElementException:
            return

    def agent_company_name(self):
        """return string of the name of the real-estate company which offer the house for sale"""
        try:
            return self.driver.find_element_by_class_name('company-name').text
        except NoSuchElementException:
            return

    def agent_company_phone(self):
        """return string of the phone number of the real-estate company which offer the house for sale"""
        try:
            return self.driver.find_element_by_class_name('company-phone').text
        except NoSuchElementException:
            return

    def agent_company_address(self):
        """Return string of the address of the real-estate company which offer the house for sale"""
        try:
            return self.driver.find_element_by_class_name('company-address').text
        except NoSuchElementException:
            return

    def description(self):
        "Return a string of the house description"
        try:
            return self.driver.find_element_by_class_name('class="description-body').text
        except NoSuchElementException:
            return

    def info_data(self):
        """
        Get the informative data regarding the propary
        :return: list of table of relevant data
        """
        return self.full_address(), self.just_listed_status(), \
               self.reo_id(), self.mls_id(), self.agent_name(),\
               self.agent_phone(), self.agent_company_name(), \
               self.agent_company_phone(), self.agent_company_address(), \
               self.description()

    def table_data(self):
        """
        Get the data regarding the propary from all tables in that page
        :return: List of tuples with the relevant data
        """
        table_values = [ele.text for ele in self.driver.find_elements_by_class_name('attr-value')]
        table_label = [ele.text for ele in self.driver.find_elements_by_class_name('attr-label')]
        zip_list = list(zip(table_label, table_values))
        data_dict = {}
        money_to_float = ['Price', 'Living Area Size', 'HOA Fees']
        str_to_float = ['Bedrooms' ,'Bathrooms' ,'Full Baths' ,'Total Rooms']
        str_to_int = ['Half Baths']
        for a, b in zip_list:
            a = a.strip(' ').strip(':').strip(' ')
            if a in money_to_float:
                b = float(b[1:].replace(',',''))
            elif a in str_to_float:
                b = float(b.replace(',',''))
            elif a in str_to_int:
                b = int(b.replace(',',''))
            elif a == 'Lot Size':
                b = float(b.split(' ')[0])
            elif a == 'Year Built':
                b = datetime.strptime(b, '%Y')
            data_dict.update({a: b})
        return data_dict

if __name__ == '__main__':
    place = 'california'
    s = Scraper(place=place, path_to_driver= WEBDRIVER_PATH)
    place = 'california'
    url = HOMEPAGE + place + '/' + "list_v"
    s.driver_get(url)
    urls = s.get_urls()
    for idx, cell_url in enumerate(urls):
        s.driver_get(cell_url)
        print(s.table_data())
