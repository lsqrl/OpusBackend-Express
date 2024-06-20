# Here we are going to have a set of routines that fakes the data in the database such that we can showcase the features
# Prior to the cumbersome actual data selection
from faker.providers import DynamicProvider
from faker import Faker
import pandas as pd
import numpy as np
from itertools import islice
from database_creation import *

fake = Faker()

def fake_experimenter_table(num_rows):

    def get_entries():
        import requests

        url = "https://www.topuniversities.com/sites/default/files/qs-rankings-data/en/3740566_indicators.txt?1637817445?v=1637823042256"

        headers = {
            "user-agent": "Mozilla/5.0",
            "x-requested-with": "XMLHttpRequest"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        def make_pretty(entry):
            from bs4 import BeautifulSoup as Soup
            return {
                "name": Soup(entry["uni"], "html.parser").select_one(".uni-link").get_text(strip=True),
                "rank": entry["overall_rank"],
                "reputation": Soup(entry["ind_76"], "html.parser").select_one(".td-wrap-in").get_text(strip=True)
            }

        yield from map(make_pretty, response.json()["data"])

    UNIVERSITY_NAMES = []
    for entry in islice(get_entries(), 30):
        UNIVERSITY_NAMES.append(entry['name'])
    university_list = set(UNIVERSITY_NAMES)
    university_provider = DynamicProvider(
         provider_name = "university_name_generator",
         elements = university_list,
    )
    fake.add_provider(university_provider)

    name_list = [] 
    surname_list = []
    email_list = []
    insitution_list = [] 
    num = 100
    ex_list = []
    for i in range(num_rows):
        name = fake.name().split(' ')
        institution = fake.university_name_generator()
        ex_list.append(Experimenter(name=name[0], surname=name[1], 
                                    email='.'.join(name) + f"@{fake.domain_name()}",
                                    institution=institution))
    session.add_all(ex_list)
    session.commit()
 

def transaction_example():
    tranDate = [] 
    custName = []
    custEmail = []
    cardNum = [] 
    zipCode = []
    tranAmount = []
    def dummy_data(numRec):
        for i in range(numRec):
            tranDate.append(fake.date_time_between_dates ('-1y', 'now'))
        for i in range(numRec):
            name = fake.name()
            custName.append(name)
            name = name.split(' ')
            name = [n.lower() for n in name]
            custEmail.append('.'.join(name) + f"@{fake.domain_name()}")
        for i in range(numRec):
            cardNum.append(fake.credit_card_number())
        for i in range(numRec):
            zipCode.append(fake.zipcode())
        for x in range(numRec):
            tranAmount.append(np.random.randint(100, 5000))
    dummy_data(100)
    df = pd.DataFrame(zip(tranDate, custName, custEmail, cardNum, zipCode, tranAmount), 
                      columns=['tranDate', 'custName', 'custEmail', 'cardNum', 'zipCode', 'tranAmount'])
    df.head(100)