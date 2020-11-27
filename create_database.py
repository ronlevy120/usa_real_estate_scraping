import mysql.connector

from passw import *


class CreateDB:
    """
    CreateDB class removing old database name 'usa_scraping_database' if exist, and creates a new one
    """
    db_connection = mysql.connector.connect(
                host=HOST,
                user=USER,
                passwd= PASS)

    db_cursor = db_connection.cursor()
    db_cursor.execute("DROP DATABASE usa_scraping_database;")
    db_cursor.execute("CREATE DATABASE IF NOT EXISTS usa_scraping_database;")

class Tables:

    def __init__(self):
        """
        Initialize Tables class.
        Defines sc as the Scraper class object and connection to the database
        """
        self.db_connection = mysql.connector.connect(
                    host=HOST,
                    user=USER,
                    passwd= PASS,
            database="usa_scraping_database")
        self.cur = self.db_connection.cursor()

    def drop_talbes_if_exist(self):
        """Delete old tables if exist"""
        self.cur.execute('drop table if exists agents;')
        self.cur.execute('drop table if exists County_Tax_Roll_Details;')
        self.cur.execute('drop table if exists Property_Tax_Roll_Details;')
        self.cur.execute('drop table if exists property_detailes;')
        self.cur.execute('drop table if exists prop_description;')
        self.cur.execute('drop table if exists company;')
        self.cur.execute('drop table if exists properties;')

    def table_properties(self):
        """Create properties table"""
        self.cur.execute('''CREATE TABLE IF NOT EXISTS properties (
         idproperties INT PRIMARY KEY AUTO_INCREMENT,
         address VARCHAR(200),
         just_list TINYINT(4),
         reo_id VARCHAR(45),
         mls_id VARCHAR(45))
        ''')
        self.cur.execute('''ALTER TABLE properties AUTO_INCREMENT = 1''')

    def table_agents(self):
        """Create agent table"""
        self.cur.execute('''CREATE TABLE IF NOT EXISTS agents (
        agent_name VARCHAR(45),
        agent_phone VARCHAR(45),
        idproperties INT,
        FOREIGN KEY(idproperties)
        REFERENCES properties(idproperties))
        ''')
    def table_company(self):
        """Create company table"""
        self.cur.execute('''CREATE TABLE IF NOT EXISTS company (
        comp_name VARCHAR(45),
        comp_phone VARCHAR(45),
        comp_address VARCHAR(45),
        idproperties INT(11),
        FOREIGN KEY (idproperties)
        REFERENCES properties (idproperties))
        ''')
    def table_prop_description(self):
        """Create prop_description table"""
        self.cur.execute('''CREATE TABLE IF NOT EXISTS prop_description (
        description VARCHAR(200),
        idproperties INT(11),
        PRIMARY KEY (idproperties),
        FOREIGN KEY (idproperties)
        REFERENCES properties (idproperties))
        ''')
    def table_property_detailes(self):
        """Create property_detailes table"""
        self.cur.execute('''CREATE TABLE IF NOT EXISTS property_detailes (
        idproperties INT(11),
        `price in us dollar` FLOAT(11),
        bedrooms FLOAT(11),
        Bathrooms FLOAT(11),
        `Full Baths` INT(11),
        `Garage Description` VARCHAR(45),
        `Basement` VARCHAR(45),
        `Total Rooms` FLOAT(11),
        `Living Area Size` FLOAT(11),
        `Lot Size in acres` FLOAT(11),
        Style VARCHAR(45),
        Exterior VARCHAR(45),
        Roof VARCHAR(45),
        Flooring VARCHAR(45),
        `Air Conditioning` VARCHAR(45),
        Utilities VARCHAR(45),
        Pool VARCHAR(45),
        `Sewer Type` VARCHAR(45),
        HOA VARCHAR(45),
        `HOA Fees is US Dollar` INT(11),
        `Year Built` DATE,
        PRIMARY KEY (idproperties),
        FOREIGN KEY (idproperties)
        REFERENCES properties (idproperties))
        ''')
    def table_Property_Tax_Roll_Details(self):
        """Create Property_Tax_Roll_Details table"""
        self.cur.execute('''CREATE TABLE IF NOT EXISTS `Property_Tax_Roll_Details` (
        `Elementary School` VARCHAR(45),
        `Junior High School` VARCHAR(45),
        `Senior High School` VARCHAR(45),
        Subdivision VARCHAR(45),
        idproperties INT(11),
        PRIMARY KEY (idproperties),
        FOREIGN KEY (idproperties)
        REFERENCES `properties` (`idproperties`))
        ''')

    def County_Tax_Roll_Details(self):
        """Create County_Tax_Roll_Details table"""
        self.cur.execute('''CREATE TABLE IF NOT EXISTS County_Tax_Roll_Details (
        `Air Conditioning` VARCHAR(45),
        Bedrooms FLOAT(11),
        Fireplaces VARCHAR(45),
        `Half Baths` INT(11),
        `Property Type` VARCHAR(45),
        APN VARCHAR(45),
        Baths FLOAT(11),
        `Construction Type` VARCHAR(45),
        `Full Baths` INT(11),
        `Land Area` FLOAT(11),
        `Num_of Stories` INT(11),
        `idproperties` INT(11),
        PRIMARY KEY (idproperties),
        FOREIGN KEY (idproperties)
        REFERENCES `properties` (`idproperties`))
        ''')

if __name__ == '__main__':
    CreateDB()
    t = Tables()
    t.drop_talbes_if_exist()
    t.table_properties()
    t.table_agents()
    t.table_company()
    t.table_prop_description()
    t.table_property_detailes()
    t.table_Property_Tax_Roll_Details()
    t.County_Tax_Roll_Details()
    db_connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        passwd=PASS,
        database="usa_scraping_database")
    cur = db_connection.cursor()
    cur.execute("SHOW TABLES")
    for table in cur:
        print(table)