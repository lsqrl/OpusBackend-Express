from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.schema import CreateSchema
from sqlalchemy import func
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from data_types import *
import os

connection = None
engine = None
session = None

load_dotenv()

url = URL.create(    
    drivername="postgresql",      
    username=os.getenv("POSTGRES_USERNAME"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host="localhost",
    port=5432,
    database="postgres"
)


def init_database():
    global connection, engine, session
    engine = create_engine(url)
    connection = engine.connect()
    Base.metadata.drop_all(engine)    # drop all tables
    with engine.connect() as connection:
        # Execute raw SQL to create a schema
        for schema in ['old', 'counterparty', 'account', 'funding_sources', 
                       'deposits', 'trades', 'funding', 'market_data_system']:
            connection.execute(text(f'DROP SCHEMA IF EXISTS {schema} CASCADE')) # drop all schemas
            connection.commit()
            connection.execute(CreateSchema(schema, if_not_exists=True))
            connection.execute(text(f"GRANT CREATE ON SCHEMA {schema} TO {url.username};"))
            # allow user to work with schemas beyond public
            connection.commit()

    Base.metadata.create_all(engine)  # start over
    Session = sessionmaker(bind=engine)
    session = Session()

def print_database_state():
    global engine
    connection = engine.connect()
    inspector = inspect(engine)
    schemas = inspector.get_schema_names()

    # Iterate over each schema
    for schema in schemas:
        if schema != 'information_schema':
            # Get all tables in the schema
            tables = inspector.get_table_names(schema=schema)
            # Iterate over each table in the schema
            for table_name in tables:
                row_count = connection.execute(text(f'SELECT COUNT(*) FROM {schema}.{table_name}')).scalar()
                
                print(f"Rows: {row_count} in Table: {schema}.{table_name}")
                rows = connection.execute(text(f'SELECT * FROM {schema}.{table_name}')).fetchall()
                print(rows)


if __name__ == "__main__":
    init_database()
    
    NUMBER_OF_USERS = 10
    NUMBER_OF_POOLS = 10

    from data_faking_example import *

    # old database
    fake_user_table(session=session, num_rows=NUMBER_OF_USERS)
    fake_currency_table(session=session)
    fake_liquidity_pool_table(session=session, num_pools=NUMBER_OF_POOLS)
    fake_liquidity_pool_trans(session)
    fake_margin_account(session)
    fake_margin_account_trans(session)
    fake_option(session)
    fake_trade_log(session)

    # new database
    fake_currencies_table(session)
    fake_chains(session)

    fake_retail(session)
    fake_legal_entity(session)

    fake_account_type(session)
    fake_account(session)
    fake_bank_account(session)

    fake_instruments(session)

    fake_portfolio(session)
    # we better start with a clean database
    # fake_trades(session)
    # fake_trades_and_portfolio(session)
    
    # fake_fx_options(session)

    print_database_state()
    #session.close()     