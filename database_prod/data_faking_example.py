# Here we are going to have a set of routines that fakes the data in the database such that we can 
# showcase the features
# Prior to the cumbersome actual data selection
from datetime import datetime, date
from faker.providers import DynamicProvider
from faker import Faker
import pandas as pd
import numpy as np
import random
from itertools import islice
from data_types import *

fake = Faker()

def fake_user_table(session, num_rows):

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
    user_list = []
    for i in range(num_rows):
        # institution = fake.university_name_generator()
        user_list.append(Users(role_id=fake.random_element(elements=('Provider', 'Taker', 'Both')),
            wallet_address=b'\x00' + fake.binary(length=20),  # Example 20-byte address
            name=fake.name(),
            password=fake.password(),
            address=fake.address(),
            age=fake.random_int(min=18, max=99),
            gender=fake.random_element(elements=('Male', 'Female', 'Non-binary', 'Other')),
            email=fake.email(),
            kyc_aml_id=fake.binary(length=30)))  # Example binary content for a KYC/AML file
    session.add_all(user_list)
    session.commit()
 
def fake_currency_table(session):
    # Create and add fake data to the session
    CURRENCY_NAMES = ['Euro', 'Mexican Peso', 'Bitcoin', 'Ethereum']
    CURRENCY_ABBREVIATIONS = ['EUR', 'MXN', 'BTC', 'ETH']
    for n, a in zip(CURRENCY_NAMES, CURRENCY_ABBREVIATIONS):
        session.add(Currency(name=n, abbreviation=a))  
        session.commit()

def fake_liquidity_pool_table(session, num_pools):
    def create_fake_liquidity_pool():
        currency_ids = session.query(Currency.id).all()
        return LiquidityPool(
            currency_id=random.choice(currency_ids)[0], # since it returns a tuple
        )

    # Create and add fake data to the session
    for _ in range(num_pools):
        fake_liquidity_pool = create_fake_liquidity_pool()
        session.add(fake_liquidity_pool)
        session.commit()

def fake_liquidity_pool_trans(session):
    pass

def fake_margin_account(session):
    pass

def fake_margin_account_trans(session):
    pass

def fake_option(session):
    pass

def fake_trade_log(session):
    pass

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

def fake_retail(session):
    new_retail_record = Retail(
        name="Alice Smith",
        onboarding_datetime=datetime.strptime('2024-07-23T14:20:00', '%Y-%m-%dT%H:%M:%S'),
        email="alice.smith@gmail.com",
        telephone_number="+1-123-45-67",
        address_of_residence="217 W Dunklin Street, Jefferson City, MO 65101",
        country_of_residence="United States of America",
        citizenship="United States of America",
        gender="Female",
        birth_date=date(1990, 5, 15),  # Using a specific date format (YYYY-MM-DD)
        ssn="123-45-6789",
        dossier_id="D-0001"
    )
    session.add(new_retail_record)
    session.commit()


def fake_legal_entity(session):
    new_legal_entity_record = Institutional(
        legal_entity_name="Lemma Finance Ltd",
        onboarding_datetime=datetime.strptime('2024-07-23T14:20:00', '%Y-%m-%dT%H:%M:%S'),
        email="support@lemma.io",
        telephone_number="+41 12345678",
        legal_address="4 Times Square, New York, NY 12345",
        country_of_incorporation="United States of America",
        dossier_id="6523416"
    )

    session.add(new_legal_entity_record)
    session.commit()

def fake_account_type(session):
    for type in ['Depositor', 'System']:   
        account_type = AccountType(name=type)
        session.add(account_type)
        session.commit()

def fake_account(session):
    new_account = Account(counterparty_id=1, counterparty_type='Institutional', type_id=1, 
                          opening_time='2024-08-14 00:00:00', active=True, closing_time='2999-12-31 00:00:00', trade_enabled=True)
    session.add(new_account)
    session.commit()

def fake_bank_account(session):
    new_account = BankAccount(counterparty_id=1, counterparty_type='Institutional', number=100, 
                              bank_name='UBS', bank_address='Switzerland', swift_bic_code='WB542MC4', iban='SW173821784198')
    session.add(new_account)
    session.commit()

def fake_currencies_table(session):
    CURRENCY_NAMES = ['USD', 'EUR', 'MXN', 'BTC', 'ETH']
    IS_TRAD_FI = [True, True, True, False, False]
    for n, a in zip(CURRENCY_NAMES, IS_TRAD_FI):
        session.add(Currencies(name=n, trad_fi=a))  
        session.commit()

def fake_chains(session):
    CHAIN_NAMES = ['Mainnet', 'Solana', 'Arbitrum']
    CHAIN_IDS = [1, None, 42161]
    CHAIN_URLS = ['https://mainnet.infura.io/v3/',
                  'https://api.mainnet-beta.solana.com',
                  'https://arb1.arbitrum.io/rpc']
    for n, id, u in zip(CHAIN_NAMES, CHAIN_IDS, CHAIN_URLS):
        chain = Chain(name=n, chain_id=id, url=u)
        session.add(chain)
        session.commit()

def fake_instruments(session):
    instruments = [
        "Name",
        "Fiat Funding",
        "Crypto Funding",
        "Loans",
        "FX Spot",
        "Crypto Spot",
        "FX Option",
        "Crypto Option",
        "FX Forwards",
        "Crypto Perpetuals"
    ]
    for i in instruments:
        session.add(Instrument(name=i))
        session.commit()

def fake_trades_and_portfolio(session):
    # Demo: add all trades to Portfolio
    target_trades = session.query(Trade).all()
    portfolio = Portfolio(name="Test")
    for trade in target_trades:
        portfolio.trades.append(trade)
    session.add(portfolio)
    session.commit()


def fake_trades(session):
    # Instruments that are target for the demo
    target_instrument_ids = session.query(Instrument.id).filter(Instrument.name.in_(["FX Option", "Fiat Funding", "FX Spot"])).all()
    for id in target_instrument_ids:
        trade = Trade(instrument_id=id[0])
        session.add(trade)
        session.commit()



def fake_fx_options(session):
    """
    so trades ID is in the Trades table
    so the flow is
    - define the Instruments table, which must contains the FX Option, Funding and FX Spot at least
    - define a test portfolio "Test" or so, in the Portfolios table
    - add a row in the Trades table with Instrument ID = the ID of Options in Instruments table
    - add a row in the Options table with Trade ID = the ID of the entry you just entered in the Trades table
    - finally, add the same Trade ID in the Portfolio table
    all this should be done via a single function
    """
    trade_id = session.query(Trade.id).join(Instrument).filter(Instrument.name.in_(["FX Option",])).all()[0][0]
    bank_account_id = session.query(BankAccount.id).join(Retail, Retail.id == BankAccount.counterparty_id).filter(Retail.name=="Alice Smith").all()[0][0]
    option = FXOptions(id=1, trade_id=trade_id, underlying_id=1, accounting_id=1, bank_account_id=bank_account_id, premium_currency_id=1, type='Call', direction='sell',
              notional=1000000, strike=1.1) # trade_time, premium_settlement_date and expiry_time we can leave as the default
    
    session.add(option)
    session.commit()