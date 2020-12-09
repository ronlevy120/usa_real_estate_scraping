from detailes_cond import *


class Sql:
    def __init__(self, cur, sc):
        """
        Initialize Sql class.
        Defines sc as the Scraper class object and the cursor as cur
        """
        self.cur = cur
        self.sc = sc

    def check_duplicates(self):
        self.cur.execute("""SELECT count(*) as count
        FROM properties
        WHERE reo_id = %s
        AND mls_id = %s
        AND update_date = %s""", [self.sc.reo_id(), self.sc.mls_id(), self.sc.update_date()])
        if self.cur.fetchall()[0][0] == 0:
            return True
        return False


    def sql_properties(self):
        """Insert values into properties table"""
        self.cur.execute("""INSERT INTO properties (
                    address, just_list, reo_id, mls_id, update_date )
                    VALUES (%s, %s, %s, %s, %s)""", [self.sc.full_address(), self.sc.just_listed_status(),
                                                self.sc.reo_id(), self.sc.mls_id(), self.sc.update_date()])
        self.last_id = self.cur.lastrowid
        print(f"last id: {self.last_id}")

    def sql_agents(self):
        """Insert values into agents table"""
        self.cur.execute("""INSERT INTO agents (idproperties, agent_name ,agent_phone)
                    VALUES (%s ,%s, %s)""", [self.last_id, self.sc.agent_name(), self.sc.agent_phone()])

    def sql_company(self):
        """Insert values into company table"""
        self.cur.execute("""INSERT INTO company (
            idproperties, comp_name, comp_phone, comp_address)
            VALUES (%s, %s, %s, %s)""", [self.last_id, self.sc.agent_company_name(),
                                         self.sc.agent_company_phone(), self.sc.agent_company_address()])

    def sql_prop_description(self):
        """Insert values into prop_description table"""
        self.cur.execute("""INSERT INTO prop_description (
            description, idproperties)
            VALUES (%s, %s)""", [self.sc.description(), self.last_id])

    def property_detailes(self):
        """Insert values into property_detailes table"""
        data_dict = self.sc.table_data()
        self.cur.execute("""INSERT INTO property_detailes (
                    idproperties, `price in us dollar`, Bedrooms, Bathrooms,
                    `Full Baths`, `Garage Description`, `Basement`, `Living Area Size`,
                    `Lot Size in acres`, `Exterior`, `Flooring`,
                    `Air Conditioning`, `Utilities`, `Pool`, `Sewer Type`, `HOA`,
                    `HOA Fees is US Dollar`, `Year Built`)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                     %s, %s, %s, %s, %s, %s, %s)""", [self.last_id, price(data_dict), bedrooms(data_dict),
                                                      bathrooms(data_dict), full_bath(data_dict), gar(data_dict),
                                                      bsm(data_dict), living(data_dict), lot_size(data_dict),
                                                      ext(data_dict), flooring(data_dict), ac(data_dict),
                                                      util(data_dict), pool(data_dict), sewer(data_dict), hoa(data_dict),
                                                      hoa_fees(data_dict), year_built(data_dict)])

    def Property_Tax_Roll_Details(self):
        """Insert values into Property_Tax_Roll_Details table"""
        data_dict = self.sc.table_data()
        self.cur.execute("""INSERT INTO Property_Tax_Roll_Details (
        idproperties, `Elementary School`, `Junior High School`, `Senior High School`,
        `Subdivision`)
        VALUES (%s, %s, %s, %s, %s)""", [self.last_id, elementary_school(data_dict),
                                         junior_high_School(data_dict), senior_high_school(data_dict), subdivision(data_dict)])

    def County_Tax_Roll_Details(self):
        """Insert values into County_Tax_Roll_Details table"""
        data_dict = self.sc.table_data()
        self.cur.execute("""INSERT INTO County_Tax_Roll_Details (
            idproperties, `Fireplaces`, `Half Baths`,
            `Property Type`, `APN`, `Baths`, `Construction Type`,
            `Land Area`, `Num_of Stories`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", [self.last_id, fire(data_dict), half_b(data_dict),
                                                                         prop_type(data_dict), apn(data_dict),
                                                                         bath(data_dict), const_type(data_dict),
                                                                         land_area(data_dict), stories(data_dict)])
