import logging
import os

import mysql.connector

from ArgParseInput import ArgParseInput
from create_database import NewDB, Tables
from myconstants import *
from passw import *
from save_to_database import SaveToDatabase
from scraper import Scraper
from stocks_api import PortfolioBuilder


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
        # reading the arguments input
        self.page = None
        self.url = None
        self.db = None
        self.sc = None
        self.place = None
        self.ar = ArgParseInput()
        logging.info(f'An ARgParseInput object was successfully made')

        self.restart = self.ar.argp()[3]
        self.database()

        # getting the places argument (list)
        self.places = self.ar.argp()[0]  # scrap those places
        logging.info(f'A places instance was successfully made out of ARgParseInput')
        logging.debug(f'Places len: {len(self.places)}')

        # getting the search_limit argument
        self.search_limit = self.ar.argp()[1]
        logging.debug(f'Search limit: {self.search_limit}')
        if self.search_limit == 9999:
            self.search_limit = 'Unlimited search'
        print(f"limit pages up to page number: {self.search_limit}")

        # getting the years argument (for the stocks chart)
        self.years = self.ar.argp()[2]
        logging.debug(f'years: {self.years}')
        if self.years < 1 or self.years > 50:
            print(f"error showing US real estate main stocks performance chart for the last {self.years} years "
                  f"\ninvalid input - should be an integer between [1-50]")
            logging.error(f'invalid input: {self.years}, should be an integer between [1-50]')
        else:
            try:
                SaveToDatabase().add_stocks(self.years)
                logging.debug(f'stocks data was added the database with the following yearS: {self.years}')
                self.pb = PortfolioBuilder(self.years)
                print(f"""showing US real estate main stocks performance for the last {self.years} years.
Average yield among selected stocks: {self.pb.average_yield()[0]} %""")
            except ResourceWarning as e:
                logging.error(f'error getting stocks_api data - ', e)


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
            logging.info(f'An instance was successfully made out of SaveToDatabase')
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
        # page_str = str(self.page)  # So we can use the page as string, later we'll change to int back
        if not os.path.exists(os.path.join(self.place, str(self.page))):
            os.mkdir(os.path.join(self.place, str(self.page)))
        urls = self.sc.get_urls()  # List of all the url in that page
        for idx, cell_url in enumerate(urls):
            logging.info(f'Url from page is under process')
            logging.debug(f"Page number: {str(self.page)}")
            inner_folder = self.sc.make_inner_folder(idx, cell_url, str(self.page))
            logging.debug(f"Image folder name:{inner_folder}")
            self.sc.driver_get(cell_url)
            self.sc.get_image(inner_folder=inner_folder, page=str(self.page))
            logging.debug(f"The photos has been downloaded")
            print(self.sc.info_data())
            logging.debug(f"Info data has been processed. len: {len(self.sc.info_data())}")
            print(self.sc.table_data())
            logging.debug(f"Table data has been processed. len: {len(self.sc.table_data())}")
            self.db.add_data_to_database()  # Making SQL Query from the data
            logging.info(f"Success! data has been inserted into SQL tables")
        self.sc.driver_get(self.url)
        print(f"End of loop {str(self.page) }")
        self.page = int(self.page)
        self.page += 1

    def database(self):
        ndb = NewDB()
        if self.restart == 'restart':
            print("Restarting database")
            ndb.delete_old()
        ndb.create_new()
        t = Tables()
        # t.drop_tables_if_exist()
        t.table_properties()
        t.table_agents()
        t.table_company()
        t.table_prop_description()
        t.table_property_details()
        t.table_property_tax_roll_details()
        t.county_tax_roll_details()
        t.real_estate_funds()
        t.property_agent()
        t.company_agent()
        t.company_property()
        db_connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            passwd=PASS,
            database="usa_scraping_database")
        cur = db_connection.cursor()

        # test for aws server permissionsoption
        # cur.execute("GRANT ALL PRIVILEGES ON mynewdatabase.* TO 'myuser'@'localhost' WITH GRANT OPTION;")

        cur.execute("SHOW TABLES")
        print("TABLES IN THE DATABASE:")
        for table in cur:
            print(table)


if __name__ == '__main__':
    main = Main()
    main.run()
