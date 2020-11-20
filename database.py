import sqlite3
import os
import contextlib

DB_FILENAME = 'usa_scraping_database.db'

if os.path.exists(DB_FILENAME):
    os.remove(DB_FILENAME)

with contextlib.closing(sqlite3.connect(DB_FILENAME)) as con:  # auto-closes
    with con:  # auto-commits
        cur = con.cursor()
        cur.execute('pragma foreign_keys')
        cur.executescript('drop table if exists agents;')
        cur.executescript('drop table if exists County_Tax_Roll_Details;')
        cur.executescript('drop table if exists Property_Tax_Roll_Details;')
        cur.executescript('drop table if exists property_detailes;')
        cur.executescript('drop table if exists images;')
        cur.executescript('drop table if exists prop_description;')
        cur.executescript('drop table if exists company;')
        cur.executescript('drop table if exists properties;')
        cur.execute('''CREATE TABLE IF NOT EXISTS `agents` (
        `idagents` INT(11) NOT NULL,
        `agent_name` VARCHAR(45) NULL DEFAULT NULL,
        `agent_phone` VARCHAR(45) NULL DEFAULT NULL,
        `idproerties` INT(11) NULL DEFAULT NULL,
        PRIMARY KEY (`idagents`),
        FOREIGN KEY (`idproerties`)
        REFERENCES `properties` (`idproperties`))
        ''')
        cur.execute('''CREATE TABLE IF NOT EXISTS `properties` (
        idproperties INT(11) NOT NULL,
        address VARCHAR(45) NULL DEFAULT NULL,
        just_list TINYINT(4) NULL DEFAULT NULL,
        reo_id VARCHAR(45) NULL DEFAULT NULL,
        mls_id VARCHAR(45) NULL DEFAULT NULL,
        PRIMARY KEY (`idproperties`))
        ''')
        cur.execute('''CREATE TABLE IF NOT EXISTS `company` (
        idcompany INT(11) NOT NULL,
        comp_name VARCHAR(45) NULL DEFAULT NULL,
        comp_phone VARCHAR(45) NULL DEFAULT NULL,
        comp_address VARCHAR(45) NULL DEFAULT NULL,
        idproperties INT(11) NULL DEFAULT NULL,
        PRIMARY KEY (`idcompany`),
        FOREIGN KEY (`idproperties`)
        REFERENCES `properties` (`idproperties`))
        ''')
        cur.execute('''CREATE TABLE IF NOT EXISTS prop_description (
        idprop_description INT(11) NOT NULL,
        description VARCHAR(200) NULL DEFAULT NULL,
        idproperties INT(11) NULL DEFAULT NULL,
        PRIMARY KEY (`idprop_description`),
        FOREIGN KEY (`idproperties`)
        REFERENCES `properties` (`idproperties`))
        ''')
        cur.execute('''CREATE TABLE IF NOT EXISTS images (
        idimages INT(11) NOT NULL,
        img_name VARCHAR(45) NULL DEFAULT NULL,
        folder VARCHAR(45) NULL DEFAULT NULL,
        page VARCHAR(45) NULL DEFAULT NULL,
        place VARCHAR(45) NULL DEFAULT NULL,
        idproperties INT(11) NULL DEFAULT NULL,
        FOREIGN KEY (`idproperties`)
        REFERENCES `properties` (`idproperties`))
        ''')
        cur.execute('''CREATE TABLE IF NOT EXISTS property_detailes (
        id_property_detailes INT(11) NOT NULL,
        idproperties INT(11) NULL DEFAULT NULL,
        price FLOAT(11) NULL DEFAULT NULL,
        bedrooms FLOAT(11) NULL DEFAULT NULL,
        Bathrooms FLOAT(11) NULL DEFAULT NULL,
        `Full Baths` INT(11) NULL DEFAULT NULL,
        `Garage Description` VARCHAR(45) NULL DEFAULT NULL,
        `Basement` TINYINT(4) NULL DEFAULT NULL,
        `Total Rooms` FLOAT(11) NULL DEFAULT NULL,
        `Living Area Size` FLOAT(11) NULL DEFAULT NULL,
        `Lot Size in acres` FLOAT(11) NULL DEFAULT NULL,
        `Style` VARCHAR(45) NULL DEFAULT NULL,
        `Exterior` VARCHAR(45) NULL DEFAULT NULL,
        `Roof` VARCHAR(45) NULL DEFAULT NULL,
        `Flooring` VARCHAR(45) NULL DEFAULT NULL,
        `Air Conditioning` VARCHAR(45) NULL DEFAULT NULL,
        `Utilities` VARCHAR(45) NULL DEFAULT NULL,
        `Pool` VARCHAR(45) NULL DEFAULT NULL,
        `Sewer Type` VARCHAR(45) NULL DEFAULT NULL,
        `HOA` TINYINT(4) NULL DEFAULT NULL,
        `HOA Fees is US Dollar` INT(11) NULL DEFAULT NULL,
        `Year Built` DATE NULL DEFAULT NULL,
        PRIMARY KEY (`id_property_detailes`),
        FOREIGN KEY (`idproperties`)
        REFERENCES `properties` (`idproperties`))
        ''')
        cur.execute('''CREATE TABLE IF NOT EXISTS `Property_Tax_Roll_Details` (
        `idProperty Tax Roll Details` INT(11) NOT NULL,
        `Elementary School` VARCHAR(45) NULL DEFAULT NULL,
        `Junior High School` VARCHAR(45) NULL DEFAULT NULL,
        `Senior High School` VARCHAR(45) NULL DEFAULT NULL,
        `Subdivision` VARCHAR(45) NULL DEFAULT NULL,
        `idproperties` INT(11) NULL DEFAULT NULL,
        PRIMARY KEY (`idProperty Tax Roll Details`),
        FOREIGN KEY (`idproperties`)
        REFERENCES `properties` (`idproperties`))
        ''')
        cur.execute('''CREATE TABLE IF NOT EXISTS `County_Tax_Roll_Details` (
        `idCounty_Tax_Roll_Details` INT(11) NOT NULL,
        `Air Conditioning` VARCHAR(45) NULL DEFAULT NULL,
        `Bedrooms` FLOAT(11) NULL DEFAULT NULL,
        `Fireplaces` TINYINT(4) NULL DEFAULT NULL,
        `Half Baths` INT(11) NULL DEFAULT NULL,
        `Property Type` VARCHAR(45) NULL DEFAULT NULL,
        `APN` VARCHAR(45) NULL DEFAULT NULL,
        `Baths` FLOAT(11) NULL DEFAULT NULL,
        `Construction Type` VARCHAR(45) NULL DEFAULT NULL,
        `Full Baths` INT(11) NULL DEFAULT NULL,
        `Land Area` FLOAT(11) NULL DEFAULT NULL,
        `Num_of Stories` INT(11) NULL DEFAULT NULL,
        `idproperties` INT(11) NULL DEFAULT NULL,
        PRIMARY KEY (`idCounty_Tax_Roll_Details`),
        FOREIGN KEY (`idproperties`)
        REFERENCES `properties` (`idproperties`))
        ''')
