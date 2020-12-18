import mysql.connector

from passw import *


class NewDB:
    """
    CreateDB class removing old database name 'usa_scraping_database' if exist, and creates a new one
    """
    def __init__(self):
        self.db_connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            passwd=PASS)
        self.db_cursor = self.db_connection.cursor()

    def create_new(self):
        self.db_cursor.execute("CREATE DATABASE IF NOT EXISTS usa_scraping_database;")

    def delete_old(self):
        self.db_cursor.execute("DROP DATABASE IF EXISTS usa_scraping_database;")


class Tables:

    def __init__(self):
        """
        Initialize Tables class.
        Defines sc as the Scraper class object and connection to the database
        """
        self.db_connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            passwd=PASS, database="usa_scraping_database")
        self.cur = self.db_connection.cursor()

    def drop_tables_if_exist(self):
        """Delete old tables if exist"""
        self.cur.execute('drop table if exists agents;')
        self.cur.execute('drop table if exists County_Tax_Roll_Details;')
        self.cur.execute('drop table if exists Property_Tax_Roll_Details;')
        self.cur.execute('drop table if exists property_details;')
        self.cur.execute('drop table if exists prop_description;')
        self.cur.execute('drop table if exists company;')

    def table_properties(self):
        """Create properties table"""
        self.cur.execute('''CREATE TABLE IF NOT EXISTS properties (
         idproperties INT PRIMARY KEY AUTO_INCREMENT,
         address VARCHAR(200),
         just_list VARCHAR(45),
         reo_id VARCHAR(45),
         mls_id VARCHAR(45),
         update_date VARCHAR (200))
        ''')
        self.cur.execute('''ALTER TABLE properties AUTO_INCREMENT = 1''')

    def table_agents(self):
        """Create agent table"""
        self.cur.execute('''CREATE TABLE IF NOT EXISTS agents (
        idagents INT PRIMARY KEY AUTO_INCREMENT,
        agent_name VARCHAR(45),
        agent_phone VARCHAR(45),
        idproperties INT,
        FOREIGN KEY(idproperties)
        REFERENCES properties(idproperties))
        ''')

    def table_company(self):
        """Create company table"""
        self.cur.execute('''CREATE TABLE IF NOT EXISTS company (
        idcompany INT PRIMARY KEY AUTO_INCREMENT,
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
        idprop_desc INT PRIMARY KEY AUTO_INCREMENT,
        description VARCHAR(200),
        idproperties INT(11),
        FOREIGN KEY (idproperties)
        REFERENCES properties (idproperties))
        ''')

    def table_property_details(self):
        """Create property_detailes table"""
        self.cur.execute('''CREATE TABLE IF NOT EXISTS property_detailes (
        idprop_details INT PRIMARY KEY AUTO_INCREMENT,
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
        FOREIGN KEY (idproperties)
        REFERENCES properties (idproperties))
        ''')

    def table_property_tax_roll_details(self):
        """Create Property_Tax_Roll_Details table"""
        self.cur.execute('''CREATE TABLE IF NOT EXISTS `Property_Tax_Roll_Details` (
        idtax_details INT PRIMARY KEY AUTO_INCREMENT,
        `Elementary School` VARCHAR(45),
        `Junior High School` VARCHAR(45),
        `Senior High School` VARCHAR(45),
        Subdivision VARCHAR(45),
        idproperties INT(11),
        FOREIGN KEY (idproperties)
        REFERENCES `properties` (`idproperties`))
        ''')

    def county_tax_roll_details(self):
        """Create County_Tax_Roll_Details table"""
        self.cur.execute('''CREATE TABLE IF NOT EXISTS County_Tax_Roll_Details (
        idcounty_details INT PRIMARY KEY AUTO_INCREMENT,
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
        FOREIGN KEY (idproperties)
        REFERENCES `properties` (`idproperties`))
        ''')

    def real_estate_funds(self):
        """
        Create table with the return of real estate funds over the years.
        The idea is the real estate investors will find it very useful to compare
        the yield over property against the stock change.
        """
        self.cur.execute('''CREATE TABLE IF NOT EXISTS funds (
        idfunds INT PRIMARY KEY AUTO_INCREMENT,
        `yield_over_years %` FLOAT(11),
        funds_companies VARCHAR(200),
        from_date DATE,
        to_date DATE)
        ''')
