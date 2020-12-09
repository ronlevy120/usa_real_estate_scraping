import os

from ArgParseInput import ArgParseInput
from myconstants import *
from passw import *
from save_to_database import SaveToDatabase
from scraper import Scraper
import logging

logging.basicConfig(handlers=[logging.FileHandler('scraping.log', 'w', 'utf-8')],
                    format="%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s",
                    datefmt='%m-%d %H:%M',
                    level=logging.INFO)


class Main:

    def __init__(self):
        """
        Initialize Main class.
        Defines sc as the Scraper class object, ar as the ArgParseInput class object,
        and the limits on the search
        """
        self.ar = ArgParseInput()
        logging.info(f'An ARgParseInput object was successfully made')
        self.places = self.ar.argp()[0]  # scrap those places
        logging.info(f'A places instance was successfully made out of ARgParseInput')
        logging.debug(f'Places len: {len(self.places)}')
        self.search_limit = self.ar.argp()[1]
        logging.debug(f'Search limit: {self.search_limit}')
        if self.search_limit == 9999:
            self.search_limit = 'Unlimited search'
        print(f"limit pages up to page number: {self.search_limit}")

    @staticmethod
    def make_folder(name):
        """
        Creates a folder.
        :name Folder name
        :return None
        """
        if not os.path.exists(name):
            os.mkdir(name)
            logging.info(f'A folder has been made. Folder name: {name}')

    def run(self):
        """Running the program with the imported modules"""
        for self.place in self.places:
            print(f"Looking for results in: {self.place}")
            self.sc = Scraper(place=self.place, path_to_driver=WEBDRIVER_PATH)
            logging.info(f'An instance was successfully made out of Scraper')
            self.db = SaveToDatabase(self.sc)
            logging.info(f'An instance was successfully made out of SavetToDatabase')
            self.sc.create_driver()
            self.make_folder(self.place)
            self.url = HOMEPAGE + self.place + '/' + "list_v"
            self.sc.driver_get(self.url)
            self.page = 1
            if self.search_limit == 'Unlimited search':
                # If there are any results at this page
                while self.sc.tables_len() > 3:
                    self.do_the_actual_work()
            else:
                # If there are any results at this page or limitation not exceeded
                while self.page < self.search_limit or self.sc.tables_len() > 3:
                    self.do_the_actual_work()
                
    def do_the_actual_work(self):
        """Doing the process of scraping the data and saving to database"""
        if self.page > 1:  # if it's not the first page
            self.url = HOMEPAGE + self.place + f"/{self.page}_p/list_v"
        self.sc.driver_get(self.url)
        self.page = str(self.page)  # So we can use the page as string, later we'll change to int back
        if not os.path.exists(os.path.join(self.place, self.page)):
            os.mkdir(os.path.join(self.place, self.page))
        urls = self.sc.get_urls()  # List of all the url in that page
        for idx, cell_url in enumerate(urls):
            logging.info(f'Url from page is under proccess')
            logging.debug(f"Page number: {self.page}")
            inner_folder = self.sc.make_inner_folder(idx, cell_url, self.page)
            logging.debug(f"Image folder name:{inner_folder}")
            self.sc.driver_get(cell_url)
            self.sc.get_image(inner_folder=inner_folder, page=self.page)
            logging.debug(f"The photos has been downloaded")
            print(self.sc.info_data())
            logging.debug(f"Info data has been processed. len: {len(self.sc.info_data())}")
            print(self.sc.table_data())
            logging.debug(f"Table data has been processed. len: {len(self.sc.table_data())}")
            self.db.add_data_to_database()  # Making SQL Query from the data
            logging.info(f"Success! data has been inserted into SQL tables")
        self.sc.driver_get(self.url)
        print(f"End of loop {self.page}")
        self.page = int(self.page)
        self.page += 1


main = Main()
main.run()
