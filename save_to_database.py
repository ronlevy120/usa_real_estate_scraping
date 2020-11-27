import mysql.connector

from manager import Sql
from passw import *


class SaveToDatabase:

    def __init__(self, sc):
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

    def add_data_to_database(self):
        """Adding the data from the Scraper class to the MYSQL database"""
        cur = self.db_connection.cursor()
        # cur.execute('pragma foreign_keys')
        mn = Sql(cur, self.sc)
        mn.sql_properties()
        mn.sql_agents()
        mn.sql_company()
        mn.sql_prop_description()
        mn.property_detailes()
        mn.Property_Tax_Roll_Details()
        mn.County_Tax_Roll_Details()
        self.db_connection.commit()
