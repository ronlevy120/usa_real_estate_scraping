from detailes_cond import Utility
from stocks_api import PortfolioBuilder

class Sql:
    def __init__(self, cur, place=None, sc=None):
        """
        Initialize Sql class.
        Defines sc as the Scraper class object and the cursor as cur
        """
        self.cur = cur
        self.sc = sc
        self.last_id_property = None
        self.last_id_agents = None
        self.last_id_company = None
        self.place = place

    def check_duplicates_properties(self):
        self.cur.execute("""SELECT count(*) as count
        FROM properties
        WHERE reo_id = %s
        AND mls_id = %s
        AND update_date = %s
        AND state = %s""", [self.sc.reo_id(), self.sc.mls_id(), self.sc.update_date(), self.place])
        if self.cur.fetchall()[0][0] == 0:
            return True
        return False

    def check_duplicates_agents(self):
        self.cur.execute("""SELECT count(*) as count
        FROM agents
        WHERE agent_name = %s
        AND agent_phone = %s""", [self.sc.agent_name(), self.sc.agent_phone()])
        if self.cur.fetchall()[0][0] == 0:
            return True
        return False

    def check_duplicates_company(self):
        self.cur.execute("""SELECT count(*) as count
        FROM company
        WHERE comp_name = %s
        AND comp_phone = %s
        AND comp_address = %s""", [self.sc.agent_company_name(), self.sc.agent_company_phone(),
                                   self.sc.agent_company_address()])
        if self.cur.fetchall()[0][0] == 0:
            return True
        return False

    def sql_properties(self):
        """Insert values into properties table"""
        self.cur.execute("""INSERT INTO properties (
                    address, just_list, reo_id, mls_id, update_date, state)
                    VALUES (%s, %s, %s, %s, %s, %s)""", [self.sc.full_address(), self.sc.just_listed_status(),
                                                self.sc.reo_id(), self.sc.mls_id(), self.sc.update_date(), self.place])
        self.last_id_property = self.cur.lastrowid
        print(f"last id property: {self.last_id_property}")
        return self.last_id_property

    def sql_agents(self):
        """Insert values into agents table"""
        self.cur.execute("""INSERT INTO agents (agent_name ,agent_phone)
                    VALUES (%s, %s)""", [self.sc.agent_name(), self.sc.agent_phone()])
        self.last_id_agents = self.cur.lastrowid
        print(f"last id agents: {self.last_id_agents}")

    def sql_company(self):
        """Insert values into company table"""
        self.cur.execute("""INSERT INTO company (
            comp_name, comp_phone, comp_address)
            VALUES (%s, %s, %s)""", [self.sc.agent_company_name(),
                                         self.sc.agent_company_phone(), self.sc.agent_company_address()])
        self.last_id_company = self.cur.lastrowid
        print(f"last id company: {self.last_id_company}")

    def sql_prop_description(self):
        """Insert values into prop_description table"""
        self.cur.execute("""INSERT INTO prop_description (
            description, idproperties)
            VALUES (%s, %s)""", [self.sc.description(), self.last_id_property])

    def property_details(self):
        """Insert values into property_details table"""
        data_dict = self.sc.table_data()
        self.cur.execute("""INSERT INTO property_detailes (

                    idproperties, `price in us dollar`, Bedrooms, Bathrooms,
                    `Full Baths`, `Garage Description`, `Basement`, `Living Area Size`,
                    `Lot Size in acres`, `Exterior`, `Flooring`,
                    `Air Conditioning`, `Utilities`, `Pool`, `Sewer Type`, `HOA`,
                    `HOA Fees is US Dollar`, `Year Built`)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                     %s, %s, %s, %s, %s, %s, %s)""", [self.last_id_property, Utility.price(data_dict), Utility.bedrooms(data_dict),
                                                      Utility.bathrooms(data_dict), Utility.full_bath(data_dict), Utility.gar(data_dict),
                                                      Utility.bsm(data_dict), Utility.living(data_dict), Utility.lot_size(data_dict),
                                                      Utility.ext(data_dict), Utility.flooring(data_dict), Utility.ac(data_dict),
                                                      Utility.util(data_dict), Utility.pool(data_dict),
                                                      Utility.sewer(data_dict), Utility.hoa(data_dict),
                                                      Utility.hoa_fees(data_dict), Utility.year_built(data_dict)])

    def property_tax_roll_details(self):
        """Insert values into property_tax_roll_details table"""
        data_dict = self.sc.table_data()

        self.cur.execute("""INSERT INTO property_tax_roll_details (
        idproperties, `Elementary School`, `Junior High School`, `Senior High School`,
        `Subdivision`)
        VALUES (%s, %s, %s, %s, %s)""", [self.last_id_property, Utility.elementary_school(data_dict),
                                         Utility.junior_high_school(data_dict), Utility.senior_high_school(data_dict),
                                         Utility.subdivision(data_dict)])

    def county_tax_roll_details(self):
        """Insert values into county_tax_roll_details table"""
        data_dict = self.sc.table_data()
        self.cur.execute("""INSERT INTO county_tax_roll_details (
            idproperties, `Fireplaces`, `Half Baths`,
            `Property Type`, `APN`, `Baths`, `Construction Type`,
            `Land Area`, `Num_of Stories`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", [self.last_id_property, Utility.fire(data_dict), Utility.half_b(data_dict),
                                                             Utility.prop_type(data_dict), Utility.apn(data_dict),
                                                             Utility.bath(data_dict), Utility.const_type(data_dict),
                                                             Utility.land_area(data_dict), Utility.stories(data_dict)])

    def stocks(self, years):
        self.pb = PortfolioBuilder(years)
        avg_yield, stocks_symbol_list, from_date, to_date = self.pb.average_yield()
        self.cur.execute("""INSERT INTO funds (
        `yield_over_years %`, funds_companies, from_date, to_date)
                   VALUES (%s, %s, %s, %s)""",
                         [float(avg_yield), " ,".join(stocks_symbol_list), from_date, to_date])

    def property_agents_junction(self):
        self.cur.execute("""INSERT INTO property_agent (
        idproperties, idagents) VALUES (%s, %s)""",
                         [self.last_id_property, self.last_id_agents])

    def company_agents_junction(self):
        self.cur.execute("""INSERT INTO company_agent (
        idcompany, idagents) VALUES (%s, %s)""",
                         [self.last_id_company, self.last_id_agents])

    def company_property_junction(self):
        self.cur.execute("""INSERT INTO company_property (
        idcompany, idproperties) VALUES (%s, %s)""",
                         [self.last_id_company, self.last_id_property])