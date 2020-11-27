import os

from ArgParseInput import ArgParseInput
from myconstants import *
from passw import *
from save_to_database import SaveToDatabase
from scraper import Scraper


class Main:

    def __init__(self):
        """
        Initialize Main class.
        Defines sc as the Scraper class object, ar as the ArgParseInput class object,
        and the limits on the search
        """
        self.ar = ArgParseInput()
        self.places = self.ar.argp()[0]
        self.search_limit = self.ar.argp()[1]
        if self.search_limit == 9999:
            self.search_limit = 'Unlimited search'
        print(f"limit pages up to page number: {self.search_limit}")

    def make_folder(self, name):
        """
        Creates a folder.
        :name Folder name
        :return None
        """
        if not os.path.exists(name):
            os.mkdir(name)

    def run(self):
        """Running the program with the impoted modules"""
        for self.place in self.places:
            print(f"Looking for results in: {self.place}")
            self.sc = Scraper(place= self.place, path_to_driver=WEBDRIVER_PATH)
            self.db = SaveToDatabase(self.sc)
            self.sc.create_driver()
            self.make_folder(self.place)
            self.url = HOMEPAGE + self.place + '/' + "list_v"
            self.sc.driver_get(self.url)
            self.page = 1
            if self.search_limit == 'Unlimited search':
                while self.sc.tables_len() > 3:
                    self.do_the_actual_work()
            else:
                while self.page < self.search_limit or self.sc.tables_len() <= 3:
                    self.do_the_actual_work()
                
    def do_the_actual_work(self):
        """Doing the process of scraping the data and saving to database"""
        if self.page > 1:
            self.url = HOMEPAGE + self.place + f"/{self.page}_p/list_v"
        self.sc.driver_get(self.url)
        self.page = str(self.page)
        if not os.path.exists(os.path.join(self.place, self.page)):
            os.mkdir(os.path.join(self.place, self.page))
        urls = self.sc.get_urls()
        for idx, cell_url in enumerate(urls):
            print(f"Page number: {self.page}")
            inner_folder = self.sc.make_inner_folder(idx, cell_url, self.page)
            print(f"Image folder name:{inner_folder}")
            self.sc.driver_get(cell_url)
            self.sc.get_image(inner_folder=inner_folder, page=self.page)
            print(self.sc.info_data())
            print(self.sc.table_data())
            self.db.add_data_to_database()
            print("Success!")
        self.sc.driver_get(self.url)
        print(f"End of loop {self.page}")
        self.page = int(self.page)
        self.page += 1


if __name__ == '__main__':
    main = Main()
    main.run()
