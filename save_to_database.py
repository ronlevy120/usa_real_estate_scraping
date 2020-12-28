import mysql.connector
from manager import Sql
from passw import *


class SaveToDatabase:

    def __init__(self, place=None, sc=None):
        """
        Initialize SaveToDatabase class.
        Defines sc as the Scraper class object and connection to the database
        """
        self.db_connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            passwd=PASS,
            database="usa_scraping_database"
        )
        self.sc = sc
        self.cur = self.db_connection.cursor()
        self.mn = Sql(self.cur, self.sc, place)

    def add_stocks(self, years):
        self.mn.stocks(years)
        self.db_connection.commit()

    def add_data_to_database(self):
        """Adding the data from the Scraper class to the MYSQL database"""
        if self.mn.check_duplicates_properties():
            last_property_id = self.mn.sql_properties()

            if self.mn.check_duplicates_agents():
                self.mn.sql_agents()
            if self.mn.check_duplicates_company():
                self.mn.sql_company()
            self.mn.sql_prop_description()
            self.mn.property_details()
            self.mn.property_tax_roll_details()
            self.mn.county_tax_roll_details()
            self.mn.property_agents_junction()
            self.mn.company_agents_junction()
            self.mn.company_property_junction()
            self.db_connection.commit()
        else:
            print("Property already exist in database")
        return last_property_id