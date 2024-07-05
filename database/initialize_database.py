from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import  func
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

from dataTypes import User

#engine = create_engine('sqlite:///example.db', echo=True)
Base = declarative_base()
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
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    global session
    session = Session()

if __name__ == "__main__":
    NUMBER_OF_USERS = 100
    NUMBER_OF_POOLS = 10
    init_database()
    # clear the table if it exists
    session.query(User).delete()
    session.commit()
    from data_faking_example import *
    fake_user_table(session=session, num_rows=NUMBER_OF_USERS)
    fake_currency_table(session=session)
    fake_liquidity_pool_table(session=session, num_pools=NUMBER_OF_POOLS)
    # Check if the users were written
    for user in session.query(User).order_by(User.id):
        print(user)
    user_count = session.query(func.count(User.id)).scalar()
    print(f"Number of entries in the 'users' table: {user_count}")