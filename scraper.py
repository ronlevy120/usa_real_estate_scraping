import os
import urllib.request
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from myconstants import *
import logging
import os, ssl


logging.basicConfig(handlers=[logging.FileHandler('scraping.log', 'w', 'utf-8')],
                    format="%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s",
                    datefmt='%m-%d %H:%M',
                    level=logging.INFO)
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context()


class Scraper:

    def __init__(self, place, path_to_driver):
        """Initialize Scraper class. Define place and path to the web driver"""
        self.place = place
        self.path_to_driver = path_to_driver
        self.driver = None
        logging.info(f'A scraper object was successfully made. Place: {self.place}')

    def create_driver(self):
        """Creates a driver with the path initialized at the init method"""
        self.driver = webdriver.Chrome(executable_path=self.path_to_driver)
        logging.info(f'A driver object was successfully made')

    def get_image(self, page, inner_folder):
        """
        Downloading images from a given site.
        :param inner_folder the folder where the image is store, created by make_inner_folder()
        :param page the current page in the site the scraper is working on
        :return: None. That function is just downloading the images
        """
        # soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        # img_tags = soup.find_all('img')
        # img_urls = [img['src'] for img in img_tags]
        # for j, img in enumerate(img_urls):  # All images from that location
        #     extension = img.split('.')[LAST_ELEMENT][:FULL_EXTENSTION]
        #     if extension == 'net':
        #         extension = 'png'
        #     elif extension == 'jpe':
        #         extension = 'jpeg'
        #     file_name = f"img_{j}." + extension
        #     try:
        #         urllib.request.urlretrieve(img, os.path.join(self.place, page, inner_folder, file_name))
        #         logging.info(f'An image was successfully downloaded. File name: {file_name}')
        #     except ValueError as e:
        #         logging.critical(f'The following error has occurred:{e}')
        #         pass
        return
    def tables_len(self):
        """return the len of a Selenium object"""
        table_len = len(self.driver.find_elements(By.TAG_NAME, "td"))
        logging.debug(f'Table length: {table_len}')
        return table_len

    def driver_get(self, url):
        """Update the driver to the received url"""
        self.driver.get(url)
        logging.info(f'driver.get was successfully made on the following url: {url}')

    def get_urls(self):
        """
        Get all the url's in a specific web page.
        :return: A list of all urls in that page
        """
        page_urls = self.driver.find_elements_by_css_selector(".tAddress [href]")
        urls = [cell.get_attribute('href') for cell in page_urls]  # All urls in that page
        logging.debug(f'Urls list length: {len(urls)}')
        return urls

    def make_inner_folder(self, idx, cell_url, page):
        """
        Create a folder inside the appropriate place folder
        :param idx: The index of the url from the url's list
        :param cell_url: The cell in the table which we're working on
        :param page the current page in the site the scraper is working on
        :return: the name of the folder that has been just created
        """
        inner_folder = str(idx + 1) + '__' + cell_url[HALF_URL:]
        if not os.path.exists(os.path.join(self.place, page, inner_folder)):
            os.mkdir(os.path.join(self.place, page, inner_folder))
        logging.debug(f'Returned folder name: {inner_folder}')
        return inner_folder

    def full_address(self):
        """Return the house owner full address. Converting Selenium object to text"""
        try:
            full_address = self.driver.find_element_by_class_name('fullAddress').text
            logging.info(f'Successfully returned address : {full_address}')
            return full_address
        except NoSuchElementException as e:
            logging.critical(f'The following error has occurred:{e}')
            return

    def just_listed_status(self):
        """
        the status of the listed house - weather it's just list or not.
        return True if it just listed, False otherwise
        """
        try:
            just_listed = self.driver.find_element_by_class_name('text-default').text
            logging.info(f'Successfully returned boolean regarding just_listed')
            logging.debug(f'just_listed status: {just_listed}')
            return just_listed
        except NoSuchElementException as e:
            logging.critical(f'The following error has occurred:{e}')
            return

    def reo_id(self):
        """return the reo_id of the property as a string"""
        try:
            logging.info(f'Successfully returned on reo_id')
            return self.driver.find_element_by_class_name('reoid').text.split(':')[1]
        except NoSuchElementException as e:
            logging.critical(f'The following error has occurred:{e}')
            return

    def mls_id(self):
        """return the mls_id of the property as a string"""
        try:
            logging.info(f'Successfully returned on mls_id')
            return self.driver.find_element_by_class_name('mlsid').text.split(':')[1]
        except NoSuchElementException as e:
            logging.critical(f'The following error has occurred:{e}')
            return

    def agent_name(self):
        """return string of the name of the real-estate agent who's selling the house"""
        try:
            agent_name = self.driver.find_element_by_class_name('agent-name').text
            logging.info(f'Successfully returned on agent_name')
            logging.debug(f'Agent name: {agent_name}')
            return agent_name
        except NoSuchElementException as e:
            logging.critical(f'The following error has occurred:{e}')
            return

    def agent_phone(self):
        """return string of the phone number of the real-estate agent who's selling the house"""
        try:
            agent_phone = self.driver.find_element_by_class_name('_agent-phone').text.split(':')[1]
            logging.info(f'Successfully returned on agent_phone')
            logging.debug(f'Agent phone: {agent_phone}')
            return agent_phone
        except NoSuchElementException as e:
            logging.critical(f'The following error has occurred:{e}')
            return

    def agent_company_name(self):
        """return string of the name of the real-estate company which offer the house for sale"""
        try:
            company_name = self.driver.find_element_by_class_name('company-name').text
            logging.info(f'Successfully returned on agent_company_name')
            logging.debug(f'Company name: {company_name}')
            return company_name
        except NoSuchElementException as e:
            logging.critical(f'The following error has occurred:{e}')
            return

    def agent_company_phone(self):
        """return string of the phone number of the real-estate company which offer the house for sale"""
        try:
            company_phone = self.driver.find_element_by_class_name('company-phone').text
            logging.info(f'Successfully returned on agent_company_phone')
            logging.debug(f'Company phone: {company_phone}')
            return company_phone
        except NoSuchElementException as e:
            logging.critical(f'The following error has occurred:{e}')
            return

    def agent_company_address(self):
        """Return string of the address of the real-estate company which offer the house for sale"""
        try:
            company_address = self.driver.find_element_by_class_name('company-address').text
            logging.info(f'Successfully returned on agent_company_address')
            logging.debug(f'Company address: {company_address}')
            return
        except NoSuchElementException as e:
            logging.critical(f'The following error has occurred:{e}')
            return

    def description(self):
        """Return a string of the house description"""
        try:
            desc = self.driver.find_element_by_class_name('class="description-body').text
            logging.info(f'Successfully returned on description')
            logging.debug(f'Description length: {len(desc)}')
            return desc
        except NoSuchElementException as e:
            logging.critical(f'The following error has occurred:{e}')
            return

    def info_data(self):
        """
        Get the informative data regarding the property
        :return: list of table of relevant data
        """
        logging.info(f'info_data has been Successfully called')
        return self.full_address(), self.just_listed_status(), \
            self.reo_id(), self.mls_id(), self.agent_name(),\
            self.agent_phone(), self.agent_company_name(), \
            self.agent_company_phone(), self.agent_company_address(), \
            self.description()

    def table_data(self):
        """
        Get the data regarding the property from all tables in that page
        :return: List of tuples with the relevant data
        """
        table_values = [ele.text for ele in self.driver.find_elements_by_class_name('attr-value')]
        table_label = [ele.text for ele in self.driver.find_elements_by_class_name('attr-label')]
        zip_list = list(zip(table_label, table_values))
        data_dict = {}
        money_to_float = ['Price', 'Living Area Size', 'HOA Fees']
        str_to_float = ['Bedrooms', 'Bathrooms', 'Full Baths', 'Total Rooms']
        str_to_int = ['Half Baths']
        for a, b in zip_list:
            a = a.strip(' ').strip(':').strip(' ')
            if a in money_to_float:
                b = float(b[1:].replace(',', ''))
            elif a in str_to_float:
                b = float(b.replace(',', ''))
            elif a in str_to_int:
                b = int(b.replace(',', ''))
            elif a == 'Lot Size':
                b = float(b.split(' ')[0])
            elif a == 'Year Built':
                b = datetime.strptime(b, '%Y')
            data_dict.update({a: b})
        logging.info(f'table_data has been Successfully called')
        return data_dict

    def update_date(self):
        """return string of the last update date of the real-estate property"""
        try:
            last_update = self.driver.find_element_by_id("updatedListing").text
            logging.info(f'Successfully returned on update date')
            logging.debug(f'Update date: {last_update}')
            return last_update
        except NoSuchElementException as e:
            logging.critical(f'The following error has occurred:{e}')
            return