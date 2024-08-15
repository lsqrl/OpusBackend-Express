from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from data_types import *
import os

connection = None
session = None

load_dotenv()
# probably we want to have a database and a schema per scenario we want to demo

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
    
    fake_liquidity_pool_trans(session)
    fake_margin_account(session)
    fake_margin_account_trans(session)
    fake_option(session)
    fake_trade_log(session)

    # Check if the users were written
    #for user in session.query(Users).order_by(User.id):
    #    print(user)
    user_count = session.query(func.count(Users.id)).scalar()
    print(f"Number of entries in the 'users' table: {user_count}")