class Sql:
    def __init__(self, cur, sc):
        """
        Initialize Sql class.
        Defines sc as the Scraper class object and the cursor as cur
        """
        self.cur = cur
        self.sc = sc
        self.last_id = None

    def sql_properties(self):
        """Insert values into properties table"""
        self.cur.execute("""INSERT INTO properties (
                    address, just_list, reo_id, mls_id)
                    VALUES (%s, %s, %s, %s)""", [self.sc.full_address(), self.sc.just_listed_status(),
                                                 self.sc.reo_id(), self.sc.mls_id()])
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

    def property_details(self):
        """Insert values into property_details table"""
        data_dict = self.sc.table_data()
        basement = price = bedrooms = bathrooms = full_bath = garage = living_area = lot_size = exterior =\
            flooring = air_conditioning = utilities = pool = sewer_type = HOA = HOA_fees = year_built = None
        if 'Basement' in data_dict:
            basement = data_dict['Basement']
        if 'Price' in data_dict:
            price = data_dict['Price']
        if 'Bedrooms' in data_dict:
            bedrooms = data_dict['Bedrooms']
        if 'Bathrooms' in data_dict:
            bathrooms = data_dict['Bathrooms']
        if 'Full Baths' in data_dict:
            full_bath = data_dict['Full Baths']
        if 'Garage Description' in data_dict:
            garage = data_dict['Garage Description']
        if 'Living Area Size' in data_dict:
            living_area = data_dict['Living Area Size']
        if 'Lot Size' in data_dict:
            lot_size = data_dict['Lot Size']
        if 'Flooring' in data_dict:
            flooring = data_dict['Flooring']
        if 'Exterior Wall Type' in data_dict:
            exterior = data_dict['Exterior Wall Type']
        if 'Air Conditioning' in data_dict:
            air_conditioning = data_dict['Air Conditioning']
        if 'Utilities' in data_dict:
            utilities = data_dict['Utilities']
        if 'Pool' in data_dict:
            pool = data_dict['Pool']
        if 'Sewer Type' in data_dict:
            sewer_type = data_dict['Sewer Type']
        if 'HOA' in data_dict:
            HOA = data_dict['HOA']
        if 'HOA Fees' in data_dict:
            HOA_fees = data_dict['HOA Fees']
        if 'Year Built' in data_dict:
            year_built = data_dict['Year Built']
        self.cur.execute("""INSERT INTO property_details (
                    idproperties, `price in us dollar`, Bedrooms, Bathrooms,
                    `Full Baths`, `Garage Description`, `Basement`, `Living Area Size`,
                    `Lot Size in acres`, `Exterior`, `Flooring`,
                    `Air Conditioning`, `Utilities`, `Pool`, `Sewer Type`, `HOA`,
                    `HOA Fees is US Dollar`, `Year Built`)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s)""",
                         [self.last_id, price, bedrooms, bathrooms, full_bath, garage,
                          basement, living_area, lot_size, exterior, flooring, air_conditioning,
                          utilities, pool, sewer_type, HOA, HOA_fees, year_built])

    def property_tax_roll_details(self):
        """Insert values into property_tax_roll_details table"""
        data_dict = self.sc.table_data()
        junior_high_School = elementary_school = senior_high_school = subdivision = None
        if 'Elementary School' in data_dict:
            elementary_school = data_dict['Elementary School']
        if 'Junior High School' in data_dict:
            junior_high_School = data_dict['Junior High School']
        if 'Senior High School' in data_dict:
            senior_high_school = data_dict['Senior High School']
        if 'Subdivision' in data_dict:
            subdivision = data_dict['Subdivision']
        self.cur.execute("""INSERT INTO property_tax_roll_details (
        idproperties, `Elementary School`, `Junior High School`, `Senior High School`,
        `Subdivision`)
        VALUES (%s, %s, %s, %s, %s)""", [self.last_id, elementary_school,
                                         junior_high_School, senior_high_school, subdivision])

    def county_tax_roll_details(self):
        """Insert values into county_tax_roll_details table"""
        data_dict = self.sc.table_data()
        ac = bedrooms = fire = half_b = prop_type = apn = bath =\
            const_type = full_bath = land_area = num_stories = None
        if 'Air Conditioning' in data_dict:
            ac = data_dict['Air Conditioning']
        if 'Bedrooms' in data_dict:
            bedrooms = data_dict['Bedrooms']
        if 'Fireplaces' in data_dict:
            fire = data_dict['Fireplaces']
        if 'Half Baths' in data_dict:
            half_b = data_dict['Half Baths']
        if 'Property Type' in data_dict:
            prop_type = data_dict['Property Type']
        if 'APN' in data_dict:
            apn = data_dict['APN']
        if 'Baths' in data_dict:
            bath = data_dict['Baths']
        if 'Construction Type' in data_dict:
            const_type = data_dict['Construction Type']
        if 'Full Baths' in data_dict:
            full_bath = data_dict['Full Baths']
        if 'Land Area' in data_dict:
            land_area = data_dict['Land Area']
        if 'No. of Stories' in data_dict:
            num_stories = data_dict['No. of Stories']
        self.cur.execute("""INSERT INTO county_tax_roll_details (
            idproperties, `Air Conditioning`,
            `Bedrooms`, `Fireplaces`, `Half Baths`,
            `Property Type`, `APN`, `Baths`, `Construction Type`, `Full Baths`,
            `Land Area`, `Num_of Stories`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", [self.last_id, ac, bedrooms, fire, half_b,
                                                                         prop_type, apn, bath, const_type, full_bath,
                                                                         land_area, num_stories])
