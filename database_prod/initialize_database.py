from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.schema import CreateSchema
from sqlalchemy import func
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from data_types import *
import os

connection = None
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
    engine = create_engine(url)
    global connection
    connection = engine.connect()
    Base.metadata.drop_all(engine)    # drop all
    with engine.connect() as connection:
        # Execute raw SQL to create a schema
        for schema in ['old', 'counterparty', 'account', 'funding_sources', 
                       'deposits', 'trades', 'funding', 'market_data_system']:
            connection.execute(CreateSchema(schema, if_not_exists=True))
            connection.execute(text(f"GRANT CREATE ON SCHEMA {schema} TO {url.username};"))
            # allow user to work with schemas beyond public
            connection.commit()

    Base.metadata.create_all(engine)  # start over
    Session = sessionmaker(bind=engine)
    global session
    session = Session()

if __name__ == "__main__":
    init_database()
    
    NUMBER_OF_USERS = 10
    NUMBER_OF_POOLS = 10

    from data_faking_example import *
    fake_user_table(session=session, num_rows=NUMBER_OF_USERS)
    fake_currency_table(session=session)
    fake_liquidity_pool_table(session=session, num_pools=NUMBER_OF_POOLS)
    
    # old database
    fake_liquidity_pool_trans(session)
    fake_margin_account(session)
    fake_margin_account_trans(session)
    fake_option(session)
    fake_trade_log(session)

    # new database
    fake_retail(session)
    fake_legal_entity(session)
    fake_account_type(session)
    fake_account(session)

    # Check if the users were written
    #for user in session.query(Users).order_by(User.id):
    #    print(user)
    user_count = session.query(func.count(Users.id)).scalar()
    print(f"Number of entries in the 'users' table: {user_count}")